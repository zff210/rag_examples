from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Document:
    id: str
    file_name: str
    file_path: str
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Document':
        return cls(
            id=data['id'],
            file_name=data['file_name'],
            file_path=data['file_path'],
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
