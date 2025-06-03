from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MCPServer:
    id: str
    name: str
    url: str
    description: Optional[str] = None
    auth_type: Optional[str] = None
    auth_value: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'auth_type': self.auth_type,
            'auth_value': self.auth_value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MCPServer':
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['url'],
            description=data.get('description'),
            auth_type=data.get('auth_type'),
            auth_value=data.get('auth_value'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
