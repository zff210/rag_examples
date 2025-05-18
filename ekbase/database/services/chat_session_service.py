from typing import List, Optional
from datetime import datetime
from ekbase.database.utils import Database
from ekbase.database.models.chat_session import ChatSession
from ekbase.database.services.chat_message_service import ChatMessageService
import logging

logger = logging.getLogger(__name__)

class ChatSessionService:
    def __init__(self):
        self.db = Database()
    
    async def create(self, session: ChatSession) -> ChatSession:
        """创建新的会话"""
        try:
            query = """
            INSERT INTO chat_sessions (id, summary, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """
            self.db.execute(query, (
                session.id,
                session.summary,
                session.created_at or datetime.now(),
                session.updated_at or datetime.now()
            ))
            self.db.commit()
            return await self.get_by_id(session.id)
        except Exception as e:
            logger.error(f"创建会话失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建会话失败: {str(e)}")
    
    async def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        """获取指定会话"""
        try:
            query = "SELECT * FROM chat_sessions WHERE id = ?"
            cursor = self.db.execute(query, (session_id,))
            row = cursor.fetchone()
            if row:
                message_service = ChatMessageService()
                messages = await message_service.list_by_session(session_id)
                return ChatSession.from_dict(dict(row), messages)
            return None
        except Exception as e:
            logger.error(f"获取会话失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取会话失败: {str(e)}")
    
    async def update(self, session: ChatSession) -> Optional[ChatSession]:
        """更新会话信息"""
        try:
            query = """
            UPDATE chat_sessions
            SET summary = ?, updated_at = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                session.summary,
                session.updated_at or datetime.now(),
                session.id
            ))
            self.db.commit()
            return await self.get_by_id(session.id)
        except Exception as e:
            logger.error(f"更新会话失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新会话失败: {str(e)}")
    
    async def delete(self, session_id: str) -> bool:
        """删除会话"""
        try:
            query = "DELETE FROM chat_sessions WHERE id = ?"
            self.db.execute(query, (session_id,))
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"删除会话失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"删除会话失败: {str(e)}")
    
    async def list_all(self) -> List[ChatSession]:
        """获取所有会话"""
        try:
            query = "SELECT * FROM chat_sessions ORDER BY created_at DESC"
            cursor = self.db.execute(query)
            return [ChatSession.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取会话列表失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取会话列表失败: {str(e)}") 