from typing import List, Optional
from ekbase.database.utils import Database
from ekbase.database.models.interview import Interview
import logging

logger = logging.getLogger(__name__)

class InterviewService:
    def __init__(self):
        self.db = Database()
    
    async def create(self, interview: Interview) -> Interview:
        """创建新的面试"""
        try:
            query = """
            INSERT INTO interviews (candidate_id, position_id, interviewer, start_time, end_time, 
                                  status, token)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor = self.db.execute(query, (
                interview.candidate_id,
                interview.position_id,
                interview.interviewer,
                interview.start_time,
                interview.end_time,
                interview.status,
                interview.token
            ))
            self.db.commit()
            interview.id = cursor.lastrowid
            return interview
        except Exception as e:
            logger.error(f"创建面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建面试失败: {str(e)}")
    
    async def get_by_id(self, interview_id: int) -> Optional[Interview]:
        """获取指定面试"""
        try:
            query = "SELECT * FROM interviews WHERE id = ?"
            cursor = self.db.execute(query, (interview_id,))
            row = cursor.fetchone()
            if row:
                return Interview.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"获取面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试失败: {str(e)}")
    
    async def get_by_token(self, token: str) -> Optional[Interview]:
        """通过token获取面试"""
        try:
            query = "SELECT * FROM interviews WHERE token = ?"
            cursor = self.db.execute(query, (token,))
            row = cursor.fetchone()
            if row:
                return Interview.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"通过token获取面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"通过token获取面试失败: {str(e)}")
    
    async def update(self, interview: Interview) -> Optional[Interview]:
        """更新面试信息"""
        try:
            query = """
            UPDATE interviews
            SET 
                status = ?, is_passed = ?, voice_reading = ?,
                report_content = ?, question_count = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                interview.status,
                interview.is_passed,
                interview.voice_reading,
                interview.report_content,
                interview.question_count,
                interview.id
            ))
            self.db.commit()
            return await self.get_by_id(interview.id)
        except Exception as e:
            logger.error(f"更新面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新面试失败: {str(e)}")
    
    async def delete(self, interview_id: int) -> bool:
        """删除面试"""
        try:
            query = "DELETE FROM interviews WHERE id = ?"
            self.db.execute(query, (interview_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除面试失败: {str(e)}")
    
    async def list_by_candidate(self, candidate_id: int) -> List[Interview]:
        """获取候选人的所有面试"""
        try:
            query = "SELECT * FROM interviews WHERE candidate_id = ? ORDER BY start_time DESC"
            cursor = self.db.execute(query, (candidate_id,))
            return [Interview.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取面试列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试列表失败: {str(e)}")
    
    async def get_report(self, interview_id: int) -> Optional[bytes]:
        """获取面试报告内容"""
        try:
            query = "SELECT report_content FROM interviews WHERE id = ?"
            cursor = self.db.execute(query, (interview_id,))
            row = cursor.fetchone()
            return row['report_content'] if row else None
        except Exception as e:
            logger.error(f"获取面试报告失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试报告失败: {str(e)}")
    
    async def update_status(self, interview_id: int, status: int) -> Optional[Interview]:
        """更新面试状态"""
        try:
            query = "UPDATE interviews SET status = ? WHERE id = ?"
            self.db.execute(query, (status, interview_id))
            self.db.commit()
            return await self.get_by_id(interview_id)
        except Exception as e:
            logger.error(f"更新面试状态失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新面试状态失败: {str(e)}") 
        
    async def list_all(self) -> List[Interview]:
        """获取所有面试列表"""
        try:
            query = "SELECT * FROM interviews ORDER BY start_time DESC"
            cursor = self.db.execute(query)
            return [Interview.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取所有面试列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取所有面试列表失败: {str(e)}")
        
    async def get_interview_ids_by_position_id(self, position_id: int) -> List[int]:
        """获取指定岗位的所有面试ID"""
        try:
            query = "SELECT id FROM interviews WHERE position_id = ?"
            cursor = self.db.execute(query, (position_id,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取指定岗位的所有面试ID失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取指定岗位的所有面试ID失败: {str(e)}")
    
        
    async def delete_by_position_id(self, position_id: int) -> bool:
        """删除指定岗位的所有面试"""
        try:
            query = "DELETE FROM interviews WHERE position_id = ?"
            self.db.execute(query, (position_id,))
            self.db.commit()
            return True 
        except Exception as e:
            logger.error(f"删除指定岗位的所有面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除指定岗位的所有面试失败: {str(e)}")
        
    async def delete_by_candidate_id(self, candidate_id: int) -> bool:
        """删除指定候选人的所有面试"""
        try:
            query = "DELETE FROM interviews WHERE candidate_id = ?"
            self.db.execute(query, (candidate_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除指定候选人的所有面试失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除指定候选人的所有面试失败: {str(e)}")
        
    async def get_interview_ids_by_candidate_id(self, candidate_id: int) -> List[int]:
        """获取指定候选人的所有面试ID"""
        try:
            query = "SELECT id FROM interviews WHERE candidate_id = ?"
            cursor = self.db.execute(query, (candidate_id,))
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取指定候选人的所有面试ID失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取指定候选人的所有面试ID失败: {str(e)}")

    async def update_voice_reading(self, interview: Interview):
        """更新面试语音朗读状态"""
        try:
            query = "UPDATE interviews SET voice_reading = ? WHERE id = ?"
            self.db.execute(query, (interview.voice_reading, interview.id))
            self.db.commit()
        except Exception as e:
            logger.error(f"更新面试语音朗读状态失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新面试语音朗读状态失败: {str(e)}")
