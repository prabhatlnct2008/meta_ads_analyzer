import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.database import db
from app.models.chat_conversation import ChatConversation
from app.models.chat_message import ChatMessage
from app.models.meta_connection import MetaConnection
from app.models.meta_ad_account import MetaAdAccount
from app.utils.jwt_helper import token_required
from app.services.meta_client import MetaClient
from app.services.chat_orchestrator import ChatOrchestrator

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations():
    """Get all conversations for user"""
    try:
        conversations = ChatConversation.query.filter_by(
            user_id=request.user_id
        ).order_by(ChatConversation.updated_at.desc()).all()

        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        }), 200

    except Exception as e:
        print(f"Error fetching conversations: {e}")
        return jsonify({'error': 'Failed to fetch conversations'}), 500

@chat_bp.route('/conversations', methods=['POST'])
@token_required
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        account_id = data.get('account_id')
        title = data.get('title', 'New Conversation')

        conversation = ChatConversation(
            id=str(uuid.uuid4()),
            user_id=request.user_id,
            meta_ad_account_id=account_id,
            title=title
        )

        db.session.add(conversation)
        db.session.commit()

        return jsonify({
            'conversation': conversation.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating conversation: {e}")
        return jsonify({'error': 'Failed to create conversation'}), 500

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(conversation_id):
    """Get messages for a conversation"""
    try:
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            user_id=request.user_id
        ).first()

        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404

        return jsonify({
            'conversation': conversation.to_dict(include_messages=True)
        }), 200

    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'error': 'Failed to fetch messages'}), 500

@chat_bp.route('/conversations/<conversation_id>/messages', methods=['POST'])
@token_required
def send_message(conversation_id):
    """Send a message in a conversation and get AI response"""
    try:
        data = request.get_json()
        message_content = data.get('message', '').strip()
        date_preset = data.get('date_preset', 'last_7d')

        if not message_content:
            return jsonify({'error': 'Message content is required'}), 400

        # Get conversation
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            user_id=request.user_id
        ).first()

        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404

        # Get ad account
        if not conversation.meta_ad_account_id:
            return jsonify({'error': 'No ad account linked to conversation'}), 400

        account = MetaAdAccount.query.filter_by(
            id=conversation.meta_ad_account_id,
            user_id=request.user_id
        ).first()

        if not account:
            return jsonify({'error': 'Ad account not found'}), 404

        # Get Meta connection
        connection = MetaConnection.query.get(account.meta_connection_id)
        if not connection:
            return jsonify({'error': 'Meta connection not found'}), 404

        access_token = connection.get_access_token()
        if not access_token:
            return jsonify({'error': 'Invalid access token'}), 401

        # Save user message
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role='user',
            content=message_content
        )
        db.session.add(user_message)

        # Update conversation title if it's the first message
        if len(conversation.messages) == 0:
            # Generate title from first message (first 50 chars)
            conversation.title = message_content[:50] + ('...' if len(message_content) > 50 else '')

        conversation.updated_at = datetime.utcnow()

        # Process message with chat orchestrator
        meta_client = MetaClient(access_token)
        orchestrator = ChatOrchestrator(meta_client)

        result = orchestrator.process_message(account.account_id, message_content, date_preset)
        answer = result['answer']

        # Save assistant message
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role='assistant',
            content=answer
        )
        assistant_message.set_metadata(result.get('data_used', {}))
        db.session.add(assistant_message)

        db.session.commit()

        return jsonify({
            'user_message': user_message.to_dict(),
            'assistant_message': assistant_message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error sending message: {e}")
        return jsonify({'error': f'Failed to process message: {str(e)}'}), 500

@chat_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
@token_required
def delete_conversation(conversation_id):
    """Delete a conversation"""
    try:
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            user_id=request.user_id
        ).first()

        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404

        db.session.delete(conversation)
        db.session.commit()

        return jsonify({
            'message': 'Conversation deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting conversation: {e}")
        return jsonify({'error': 'Failed to delete conversation'}), 500
