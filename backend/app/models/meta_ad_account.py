from datetime import datetime
from app.database import db

class MetaAdAccount(db.Model):
    __tablename__ = 'meta_ad_accounts'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    meta_connection_id = db.Column(db.String(36), db.ForeignKey('meta_connections.id', ondelete='CASCADE'), nullable=False)
    account_id = db.Column(db.String(255), nullable=False, index=True)  # Meta ad account ID
    name = db.Column(db.String(255))
    currency = db.Column(db.String(10))
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chat_conversations = db.relationship('ChatConversation', backref='meta_ad_account', lazy=True)

    def to_dict(self):
        """Convert ad account to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meta_connection_id': self.meta_connection_id,
            'account_id': self.account_id,
            'name': self.name,
            'currency': self.currency,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
