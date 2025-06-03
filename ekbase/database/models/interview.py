from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Interview:
    id: Optional[int]
    candidate_id: int
    position_id: int
    interviewer: str
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    status: int = 0  # 0=未开始，1=试题准备中 2=试题已备好 3=面试进行中 4=面试完毕 5=报告已生成
    question_count: Optional[int] = None
    is_passed: Optional[int] = None  # 0=未通过，1=通过
    voice_reading: int = 0  # 0=关闭，1=开启
    report_content: Optional[bytes] = None
    token: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'position_id': self.position_id,
            'interviewer': self.interviewer,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'question_count': self.question_count,
            'is_passed': self.is_passed,
            'voice_reading': self.voice_reading,
            'token': self.token
            # 不返回报告内容，因为是二进制数据
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Interview':
        return cls(
            id=data.get('id'),
            candidate_id=data['candidate_id'],
            position_id=data['position_id'],
            interviewer=data['interviewer'],
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 0),
            question_count=data.get('question_count'),
            is_passed=data.get('is_passed'),
            voice_reading=data.get('voice_reading', 0),
            report_content=data.get('report_content'),
            token=data.get('token')
        ) 