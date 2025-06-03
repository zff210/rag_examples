from dataclasses import dataclass
from typing import Optional

@dataclass
class Candidate:
    position_id: str
    name: str
    id: Optional[int] = None
    email: Optional[str] = None
    resume_type: Optional[str] = None  # PDF，WORD
    resume_content: Optional[bytes] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'position_id': self.position_id,
            'name': self.name,
            'email': self.email,
            'resume_type': self.resume_type,
            # 不返回简历内容，因为是二进制数据
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Candidate':
        return cls(
            id=data.get('id'),
            position_id=data['position_id'],
            name=data['name'],
            email=data.get('email'),
            resume_type=data.get('resume_type'),
            resume_content=data.get('resume_content')
        ) 