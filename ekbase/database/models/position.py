from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Position:
    name: str
    id: Optional[int] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    quantity: Optional[int] = None
    status: int = 0  # 0=未启动，1=进行中，2=已完成
    created_at: Optional[int] = None
    recruiter: Optional[str] = None
    link: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'requirements': self.requirements,
            'responsibilities': self.responsibilities,
            'quantity': self.quantity,
            'status': self.status,
            'created_at': self.created_at,
            'recruiter': self.recruiter,
            'link': self.link
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Position':
        return cls(
            id=data.get('id'),
            name=data['name'],
            requirements=data.get('requirements'),
            responsibilities=data.get('responsibilities'),
            quantity=data.get('quantity'),
            status=data.get('status', 0),
            created_at=data.get('created_at'),
            recruiter=data.get('recruiter'),
            link=data.get('link')
        ) 