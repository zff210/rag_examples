from dataclasses import dataclass
from typing import Optional

@dataclass
class InterviewQuestion:
    interview_id: int
    question: str
    id: Optional[int] = None
    score_standard: Optional[str] = None
    answer_audio: Optional[bytes] = None
    answer_text: Optional[str] = None
    created_at: Optional[int] = None
    answered_at: Optional[int] = None
    example_answer: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'interview_id': self.interview_id,
            'question': self.question,
            'score_standard': self.score_standard,
            'answer_text': self.answer_text,
            'created_at': self.created_at,
            'answered_at': self.answered_at,
            'example_answer': self.example_answer
            # 不返回音频内容，因为是二进制数据
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'InterviewQuestion':
        return cls(
            id=data.get('id'),
            interview_id=data['interview_id'],
            question=data['question'],
            score_standard=data.get('score_standard'),
            answer_audio=data.get('answer_audio'),
            answer_text=data.get('answer_text'),
            created_at=data.get('created_at'),
            answered_at=data.get('answered_at'),
            example_answer=data.get('example_answer')
        ) 