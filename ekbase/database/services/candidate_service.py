from typing import List, Optional
from ekbase.database.utils import Database
from ekbase.database.models.candidate import Candidate
import logging

logger = logging.getLogger(__name__)

class CandidateService:
    def __init__(self):
        self.db = Database()
    
    async def create(self, candidate: Candidate) -> bool:
        """创建新的候选人"""
        try:
            query = """
            INSERT INTO candidates (position_id, name, email, resume_type, resume_content)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor = self.db.execute(query, (
                candidate.position_id,
                candidate.name,
                candidate.email,
                candidate.resume_type,
                candidate.resume_content
            ))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"创建候选人失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建候选人失败: {str(e)}")
    
    async def get_by_id(self, candidate_id: int) -> Optional[Candidate]:
        """获取指定候选人"""
        try:
            query = "SELECT * FROM candidates WHERE id = ?"
            cursor = self.db.execute(query, (candidate_id,))
            row = cursor.fetchone()
            if row:
                return Candidate.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"获取候选人失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取候选人失败: {str(e)}")
    
    async def update(self, candidate: Candidate) -> Optional[Candidate]:
        """更新候选人信息"""
        try:
            query = """
            UPDATE candidates
            SET position_id = ?, name = ?, email = ?, resume_type = ?, resume_content = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                candidate.position_id,
                candidate.name,
                candidate.email,
                candidate.resume_type,
                candidate.resume_content,
                candidate.id
            ))
            self.db.commit()
            return await self.get_by_id(candidate.id)
        except Exception as e:
            logger.error(f"更新候选人失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新候选人失败: {str(e)}")
    
    async def delete(self, candidate_id: int) -> bool:
        """删除候选人"""
        try:
            query = "DELETE FROM candidates WHERE id = ?"
            self.db.execute(query, (candidate_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除候选人失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除候选人失败: {str(e)}")
    
    async def list_by_position(self, position_id: int) -> List[Candidate]:
        """获取指定岗位的所有候选人"""
        try:
            query = "SELECT * FROM candidates WHERE position_id = ?"
            cursor = self.db.execute(query, (position_id,))
            return [Candidate.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取候选人列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取候选人列表失败: {str(e)}")
    
    async def get_resume(self, candidate_id: int) -> Optional[Candidate]:
        """获取候选人简历"""
        try:
            query = "SELECT * FROM candidates WHERE id = ?"
            cursor = self.db.execute(query, (candidate_id,))
            row = cursor.fetchone()
            return Candidate.from_dict(dict(row)) if row else None
        except Exception as e:
            logger.error(f"获取简历内容失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取简历内容失败: {str(e)}") 
        
    async def list_all(self) -> List[Candidate]:
        """获取所有候选人列表"""
        try:
            query = "SELECT id, position_id, name, email FROM candidates ORDER BY id DESC"
            cursor = self.db.execute(query)
            return [Candidate.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取所有候选人列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取所有候选人列表失败: {str(e)}")