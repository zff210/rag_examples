from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MCPTool:
    id: str
    server_id: str
    name: str
    description: Optional[str] = None
    input_schema: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'description': self.description,
            'input_schema': self.input_schema,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MCPTool':
        return cls(
            id=data['id'],
            server_id=data['server_id'],
            name=data['name'],
            description=data.get('description'),
            input_schema=data.get('input_schema'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
