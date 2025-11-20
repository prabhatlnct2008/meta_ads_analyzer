from datetime import datetime
from app.database import db
import json

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.String(36), primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('chat_conversations.id', ondelete='CASCADE'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = db.Column(db.Text, nullable=False)
    metadata = db.Column(db.Text)  # JSON string for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_metadata(self, data):
        """Set metadata as JSON string"""
        self.metadata = json.dumps(data) if data else None

    def get_metadata(self):
        """Get metadata as dictionary"""
        return json.loads(self.metadata) if self.metadata else {}

    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
