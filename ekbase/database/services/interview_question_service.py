from typing import List, Optional
from datetime import datetime
from ekbase.database.utils import Database
from ekbase.database.models.interview_question import InterviewQuestion
import logging
import threading

logger = logging.getLogger(__name__)

class InterviewQuestionService:
    def __init__(self, use_singleton: bool = True):
        """
        初始化面试问题服务
        
        Args:
            use_singleton: 是否使用单例模式，默认为True
        """
        self._local = threading.local()
        self._use_singleton = use_singleton
    
    @property
    def db(self):
        if not hasattr(self._local, 'db'):
            self._local.db = Database(use_singleton=self._use_singleton)
        return self._local.db

    async def batch_create(self, questions: List[InterviewQuestion]):
        """批量创建面试问题"""
        try:
            query = """
            INSERT INTO interview_questions (interview_id, question, score_standard, created_at)
            VALUES (?, ?, ?, ?)
            """
            current_time = int(datetime.now().timestamp())
            for question in questions:
                self.db.execute(query, (
                    question.interview_id,
                    question.question,
                    question.score_standard,
                    current_time
                ))
            self.db.commit()
        except Exception as e:
            logger.error(f"批量创建面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"批量创建面试问题失败: {str(e)}")
        finally:
            self.db.close()
    
    async def get_by_id(self, question_id: int) -> Optional[InterviewQuestion]:
        """获取指定面试问题"""
        try:
            query = "SELECT * FROM interview_questions WHERE id = ?"
            cursor = self.db.execute(query, (question_id,))
            row = cursor.fetchone()
            if row:
                return InterviewQuestion.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"获取面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试问题失败: {str(e)}")
    
    async def update(self, question: InterviewQuestion):
        """更新面试问题信息"""
        try:
            query = """
            UPDATE interview_questions
            SET 
                answer_audio = ?, answer_text = ?, answered_at = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                question.answer_audio,
                question.answer_text,
                question.answered_at,
                question.id
            ))
            self.db.commit()
        except Exception as e:
            logger.error(f"更新面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新面试问题失败: {str(e)}")
    
    async def delete(self, question_id: int) -> bool:
        """删除面试问题"""
        try:
            query = "DELETE FROM interview_questions WHERE id = ?"
            self.db.execute(query, (question_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除面试问题失败: {str(e)}")
    
    async def list_by_interview(self, interview_id: int) -> List[InterviewQuestion]:
        """获取面试的所有问题"""
        try:
            query = "SELECT * FROM interview_questions WHERE interview_id = ? ORDER BY created_at ASC"
            cursor = self.db.execute(query, (interview_id,))
            return [InterviewQuestion.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取面试问题列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试问题列表失败: {str(e)}")
    
    async def get_answer_audio(self, question_id: int) -> Optional[bytes]:
        """获取问题回答的音频内容"""
        try:
            query = "SELECT answer_audio FROM interview_questions WHERE id = ?"
            cursor = self.db.execute(query, (question_id,))
            row = cursor.fetchone()
            return row['answer_audio'] if row else None
        except Exception as e:
            logger.error(f"获取回答音频失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取回答音频失败: {str(e)}")
    
    async def submit_answer(self, question_id: int, answer_text: str, answer_audio: Optional[bytes] = None) -> Optional[InterviewQuestion]:
        """提交问题回答"""
        try:
            current_time = int(datetime.now().timestamp())
            query = """
            UPDATE interview_questions
            SET answer_text = ?, answer_audio = ?, answered_at = ?
            WHERE id = ?
            """
            self.db.execute(query, (answer_text, answer_audio, current_time, question_id))
            self.db.commit()
            return await self.get_by_id(question_id)
        except Exception as e:
            logger.error(f"提交问题回答失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"提交问题回答失败: {str(e)}") 
    
    async def delete_by_interview_ids(self, interview_ids: List[int]) -> bool:
        """删除指定面试的所有问题"""
        try:
            query = "DELETE FROM interview_questions WHERE interview_id IN ?"
            self.db.execute(query, (interview_ids,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除面试问题失败: {str(e)}")

    async def list_by_interview_id(self, interview_id: int, page: int = 1, page_size: int = 10) -> List[InterviewQuestion]:
        """获取指定面试的所有问题
        
        Args:
            interview_id: 面试ID
            page: 页码，从1开始
            page_size: 每页问题数量，默认10个
        """
        try:
            offset = (page - 1) * page_size
            query = """
            SELECT * FROM interview_questions 
            WHERE interview_id = ? 
            ORDER BY created_at ASC 
            LIMIT ? OFFSET ?
            """
            cursor = self.db.execute(query, (interview_id, page_size, offset))
            return [InterviewQuestion.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取面试问题列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取面试问题列表失败: {str(e)}")

    async def update_example_answer(self, question_id: int, example_answer: str):
        """更新示例答案"""
        try:
            query = "UPDATE interview_questions SET example_answer = ? WHERE id = ?"
            self.db.execute(query, (example_answer, question_id))
            self.db.commit()
        except Exception as e:
            logger.error(f"更新示例答案失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新示例答案失败: {str(e)}")
    
    async def delete_by_interview_id(self, interview_id: int) -> bool:
        """删除指定面试的所有问题"""
        try:
            query = "DELETE FROM interview_questions WHERE interview_id = ?"
            self.db.execute(query, (interview_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除面试问题失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除面试问题失败: {str(e)}")