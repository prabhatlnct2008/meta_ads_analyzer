from datetime import datetime
from app.database import db
from app.utils.encryption import encrypt_token, decrypt_token

class MetaConnection(db.Model):
    __tablename__ = 'meta_connections'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    meta_user_id = db.Column(db.String(255))
    access_token_encrypted = db.Column(db.Text, nullable=False)
    token_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    meta_ad_accounts = db.relationship('MetaAdAccount', backref='meta_connection', lazy=True, cascade='all, delete-orphan')

    def set_access_token(self, token):
        """Encrypt and store access token"""
        self.access_token_encrypted = encrypt_token(token)

    def get_access_token(self):
        """Decrypt and return access token"""
        return decrypt_token(self.access_token_encrypted)

    def to_dict(self):
        """Convert connection to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meta_user_id': self.meta_user_id,
            'token_expires_at': self.token_expires_at.isoformat() if self.token_expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
