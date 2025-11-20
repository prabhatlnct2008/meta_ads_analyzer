from flask import Blueprint, request, jsonify
from app.models.meta_connection import MetaConnection
from app.models.meta_ad_account import MetaAdAccount
from app.utils.jwt_helper import token_required
from app.services.meta_client import MetaClient
from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)

def get_meta_client_for_account(user_id: str, account_id: str):
    """Helper to get MetaClient for a specific account"""
    # Get account
    account = MetaAdAccount.query.filter_by(
        id=account_id,
        user_id=user_id
    ).first()

    if not account:
        return None, None

    # Get connection
    connection = MetaConnection.query.get(account.meta_connection_id)
    if not connection:
        return None, None

    # Get access token
    access_token = connection.get_access_token()
    if not access_token:
        return None, None

    meta_client = MetaClient(access_token)
    return meta_client, account

@analytics_bp.route('/overview', methods=['GET'])
@token_required
def get_overview():
    """Get account overview analytics"""
    try:
        account_id = request.args.get('account_id')
        date_preset = request.args.get('date_preset', 'last_7d')

        if not account_id:
            return jsonify({'error': 'account_id is required'}), 400

        meta_client, account = get_meta_client_for_account(request.user_id, account_id)

        if not meta_client:
            return jsonify({'error': 'Account not found or connection invalid'}), 404

        # Get analytics
        analytics_service = AnalyticsService(meta_client)
        overview = analytics_service.get_account_overview(account.account_id, date_preset)

        return jsonify({
            'account_id': account_id,
            'account_name': account.name,
            'date_preset': date_preset,
            'overview': overview
        }), 200

    except Exception as e:
        print(f"Error in get_overview: {e}")
        return jsonify({'error': 'Failed to fetch overview analytics'}), 500

@analytics_bp.route('/campaigns', methods=['GET'])
@token_required
def get_campaigns():
    """Get campaigns with analytics"""
    try:
        account_id = request.args.get('account_id')
        date_preset = request.args.get('date_preset', 'last_7d')

        if not account_id:
            return jsonify({'error': 'account_id is required'}), 400

        meta_client, account = get_meta_client_for_account(request.user_id, account_id)

        if not meta_client:
            return jsonify({'error': 'Account not found or connection invalid'}), 404

        # Get campaigns with insights
        analytics_service = AnalyticsService(meta_client)
        campaigns = analytics_service.get_campaigns_with_insights(account.account_id, date_preset)

        return jsonify({
            'account_id': account_id,
            'account_name': account.name,
            'date_preset': date_preset,
            'campaigns': campaigns
        }), 200

    except Exception as e:
        print(f"Error in get_campaigns: {e}")
        return jsonify({'error': 'Failed to fetch campaigns'}), 500

@analytics_bp.route('/campaigns/<campaign_id>', methods=['GET'])
@token_required
def get_campaign_detail(campaign_id):
    """Get detailed view of a campaign"""
    try:
        account_id = request.args.get('account_id')
        date_preset = request.args.get('date_preset', 'last_7d')

        if not account_id:
            return jsonify({'error': 'account_id is required'}), 400

        meta_client, account = get_meta_client_for_account(request.user_id, account_id)

        if not meta_client:
            return jsonify({'error': 'Account not found or connection invalid'}), 404

        # Get campaign detail
        analytics_service = AnalyticsService(meta_client)
        detail = analytics_service.get_campaign_detail(campaign_id, date_preset)

        return jsonify({
            'account_id': account_id,
            'account_name': account.name,
            'date_preset': date_preset,
            'campaign': detail
        }), 200

    except Exception as e:
        print(f"Error in get_campaign_detail: {e}")
        return jsonify({'error': 'Failed to fetch campaign detail'}), 500
