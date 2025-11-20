from datetime import datetime
from app.database import db

class ChatConversation(db.Model):
    __tablename__ = 'chat_conversations'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    meta_ad_account_id = db.Column(db.String(36), db.ForeignKey('meta_ad_accounts.id', ondelete='SET NULL'))
    title = db.Column(db.String(255), default='New Conversation')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = db.relationship('ChatMessage', backref='conversation', lazy=True, cascade='all, delete-orphan', order_by='ChatMessage.created_at')

    def to_dict(self, include_messages=False):
        """Convert conversation to dictionary"""
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'meta_ad_account_id': self.meta_ad_account_id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

        if include_messages:
            result['messages'] = [msg.to_dict() for msg in self.messages]

        return result
