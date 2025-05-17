from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from ekbase.database.models.chat_message import ChatMessage

@dataclass
class ChatSession:
    id: str
    summary: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    messages: Optional[List[ChatMessage]] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'summary': self.summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'messages': [message.to_dict() for message in self.messages] if self.messages else None
        }
    
    @classmethod
    def from_dict(cls, data: dict, messages: Optional[List[ChatMessage]] = None) -> 'ChatSession':
        return cls(
            id=data['id'],
            summary=data.get('summary'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            messages=messages
        ) 