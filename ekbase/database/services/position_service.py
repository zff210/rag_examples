from typing import List, Optional
from datetime import datetime
from ekbase.database.utils import Database
from ekbase.database.models.position import Position
import logging

logger = logging.getLogger(__name__)

class PositionService:
    def __init__(self):
        self.db = Database()
    
    async def create(self, position: Position) -> Position:
        """创建新的岗位"""
        try:
            query = """
            INSERT INTO positions (name, requirements, responsibilities, quantity, status, created_at, recruiter, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            current_time = int(datetime.now().timestamp())
            cursor = self.db.execute(query, (
                position.name,
                position.requirements,
                position.responsibilities,
                position.quantity,
                position.status,
                current_time,
                position.recruiter,
                position.link
            ))
            self.db.commit()
            position.id = cursor.lastrowid
            position.created_at = current_time
            return position
        except Exception as e:
            logger.error(f"创建岗位失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建岗位失败: {str(e)}")
    
    async def get_by_id(self, position_id: int) -> Optional[Position]:
        """获取指定岗位"""
        try:
            query = "SELECT * FROM positions WHERE id = ?"
            cursor = self.db.execute(query, (position_id,))
            row = cursor.fetchone()
            if row:
                return Position.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"获取岗位失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取岗位失败: {str(e)}")
        
    async def list_by_ids(self, position_ids: List[int]) -> List[Position]:
        """根据岗位id列表获取岗位列表"""
        try:
            query = "SELECT * FROM positions WHERE id IN ?"
            cursor = self.db.execute(query, (position_ids,))
            return [Position.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取岗位列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取岗位列表失败: {str(e)}")  
         
    async def update(self, position: Position) -> Optional[Position]:
        """更新岗位信息"""
        try:
            query = """
            UPDATE positions
            SET name = ?, requirements = ?, responsibilities = ?, 
                quantity = ?, status = ?, recruiter = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                position.name,
                position.requirements,
                position.responsibilities,
                position.quantity,
                position.status,
                position.recruiter,
                position.id
            ))
            self.db.commit()
            return await self.get_by_id(position.id)
        except Exception as e:
            logger.error(f"更新岗位失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新岗位失败: {str(e)}")
    
    async def delete(self, position_id: int) -> bool:
        """删除岗位"""
        try:
            query = "DELETE FROM positions WHERE id = ?"
            self.db.execute(query, (position_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除岗位失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除岗位失败: {str(e)}")
    
    async def list_all(self, status: Optional[int] = None) -> List[Position]:
        """获取所有岗位，可选择按状态筛选"""
        try:
            if status is not None:
                query = "SELECT * FROM positions WHERE status = ? ORDER BY created_at DESC"
                cursor = self.db.execute(query, (status,))
            else:
                query = "SELECT * FROM positions ORDER BY created_at DESC"
                cursor = self.db.execute(query)
            return [Position.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取岗位列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取岗位列表失败: {str(e)}") 