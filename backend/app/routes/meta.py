import os
import uuid
import requests
from flask import Blueprint, request, jsonify, redirect
from datetime import datetime, timedelta
from app.database import db
from app.models.meta_connection import MetaConnection
from app.models.meta_ad_account import MetaAdAccount
from app.utils.jwt_helper import token_required
from app.services.meta_client import MetaClient

meta_bp = Blueprint('meta', __name__)

# Meta OAuth configuration
META_APP_ID = os.getenv('META_APP_ID')
META_APP_SECRET = os.getenv('META_APP_SECRET')
META_REDIRECT_URI = os.getenv('META_REDIRECT_URI', 'http://localhost:5000/api/meta/callback')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

@meta_bp.route('/connect', methods=['GET'])
@token_required
def connect():
    """Generate Meta OAuth URL"""
    try:
        # Store user_id in state parameter for callback
        state = f"{request.user_id}"

        oauth_url = (
            f"https://www.facebook.com/v19.0/dialog/oauth?"
            f"client_id={META_APP_ID}&"
            f"redirect_uri={META_REDIRECT_URI}&"
            f"state={state}&"
            f"scope=ads_read,ads_management,business_management"
        )

        return jsonify({
            'oauth_url': oauth_url
        }), 200

    except Exception as e:
        print(f"Error generating OAuth URL: {e}")
        return jsonify({'error': 'Failed to generate OAuth URL'}), 500

@meta_bp.route('/callback', methods=['GET'])
def callback():
    """Handle Meta OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')

        if error:
            return redirect(f"{FRONTEND_URL}/dashboard?error=oauth_denied")

        if not code or not state:
            return redirect(f"{FRONTEND_URL}/dashboard?error=invalid_callback")

        user_id = state

        # Exchange code for access token
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        token_params = {
            'client_id': META_APP_ID,
            'client_secret': META_APP_SECRET,
            'redirect_uri': META_REDIRECT_URI,
            'code': code
        }

        token_response = requests.get(token_url, params=token_params, timeout=30)
        token_response.raise_for_status()
        token_data = token_response.json()

        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 5184000)  # Default 60 days

        if not access_token:
            return redirect(f"{FRONTEND_URL}/dashboard?error=token_exchange_failed")

        # Exchange for long-lived token
        long_lived_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        long_lived_params = {
            'grant_type': 'fb_exchange_token',
            'client_id': META_APP_ID,
            'client_secret': META_APP_SECRET,
            'fb_exchange_token': access_token
        }

        long_lived_response = requests.get(long_lived_url, params=long_lived_params, timeout=30)
        if long_lived_response.status_code == 200:
            long_lived_data = long_lived_response.json()
            access_token = long_lived_data.get('access_token', access_token)
            expires_in = long_lived_data.get('expires_in', expires_in)

        # Get user's Meta ID
        me_url = f"https://graph.facebook.com/v19.0/me?access_token={access_token}"
        me_response = requests.get(me_url, timeout=30)
        me_response.raise_for_status()
        me_data = me_response.json()
        meta_user_id = me_data.get('id')

        # Create or update MetaConnection
        connection = MetaConnection.query.filter_by(user_id=user_id, meta_user_id=meta_user_id).first()

        if connection:
            connection.set_access_token(access_token)
            connection.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            connection.updated_at = datetime.utcnow()
        else:
            connection = MetaConnection(
                id=str(uuid.uuid4()),
                user_id=user_id,
                meta_user_id=meta_user_id,
                token_expires_at=datetime.utcnow() + timedelta(seconds=expires_in)
            )
            connection.set_access_token(access_token)
            db.session.add(connection)

        db.session.commit()

        # Fetch and store ad accounts
        try:
            meta_client = MetaClient(access_token)
            accounts = meta_client.get_user_accounts()

            for account in accounts:
                account_id = account.get('id')  # e.g., act_123456
                raw_account_id = account.get('account_id')  # e.g., 123456

                existing_account = MetaAdAccount.query.filter_by(
                    user_id=user_id,
                    account_id=account_id
                ).first()

                if existing_account:
                    existing_account.name = account.get('name')
                    existing_account.currency = account.get('currency')
                    existing_account.status = account.get('account_status')
                    existing_account.updated_at = datetime.utcnow()
                else:
                    new_account = MetaAdAccount(
                        id=str(uuid.uuid4()),
                        user_id=user_id,
                        meta_connection_id=connection.id,
                        account_id=account_id,
                        name=account.get('name'),
                        currency=account.get('currency'),
                        status=account.get('account_status', 'ACTIVE')
                    )
                    db.session.add(new_account)

            db.session.commit()

        except Exception as e:
            print(f"Error fetching ad accounts: {e}")
            # Continue even if account fetch fails

        return redirect(f"{FRONTEND_URL}/dashboard?connected=true")

    except Exception as e:
        print(f"Error in OAuth callback: {e}")
        return redirect(f"{FRONTEND_URL}/dashboard?error=connection_failed")

@meta_bp.route('/accounts', methods=['GET'])
@token_required
def get_accounts():
    """Get connected Meta ad accounts for user"""
    try:
        accounts = MetaAdAccount.query.filter_by(user_id=request.user_id).all()

        return jsonify({
            'accounts': [account.to_dict() for account in accounts]
        }), 200

    except Exception as e:
        print(f"Error fetching accounts: {e}")
        return jsonify({'error': 'Failed to fetch accounts'}), 500

@meta_bp.route('/accounts/<account_id>/refresh', methods=['POST'])
@token_required
def refresh_account(account_id):
    """Refresh data for a specific account"""
    try:
        account = MetaAdAccount.query.filter_by(
            id=account_id,
            user_id=request.user_id
        ).first()

        if not account:
            return jsonify({'error': 'Account not found'}), 404

        # Get connection and access token
        connection = MetaConnection.query.get(account.meta_connection_id)
        if not connection:
            return jsonify({'error': 'Connection not found'}), 404

        access_token = connection.get_access_token()

        # Fetch latest account data
        meta_client = MetaClient(access_token)
        accounts = meta_client.get_user_accounts()

        # Find and update this account
        for acc in accounts:
            if acc.get('id') == account.account_id:
                account.name = acc.get('name')
                account.currency = acc.get('currency')
                account.status = acc.get('account_status')
                account.updated_at = datetime.utcnow()
                db.session.commit()
                break

        return jsonify({
            'message': 'Account refreshed successfully',
            'account': account.to_dict()
        }), 200

    except Exception as e:
        print(f"Error refreshing account: {e}")
        return jsonify({'error': 'Failed to refresh account'}), 500

@meta_bp.route('/disconnect/<connection_id>', methods=['DELETE'])
@token_required
def disconnect(connection_id):
    """Disconnect a Meta connection"""
    try:
        connection = MetaConnection.query.filter_by(
            id=connection_id,
            user_id=request.user_id
        ).first()

        if not connection:
            return jsonify({'error': 'Connection not found'}), 404

        db.session.delete(connection)
        db.session.commit()

        return jsonify({
            'message': 'Connection disconnected successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error disconnecting: {e}")
        return jsonify({'error': 'Failed to disconnect'}), 500
