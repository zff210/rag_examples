from typing import List, Optional
from datetime import datetime
from ekbase.config import settings
from ekbase.database.utils import Database
from ekbase.database.models.chat_message import ChatMessage
import logging

logger = logging.getLogger(__name__)

class ChatMessageService:
    def __init__(self):
        self.db = Database()
    
    async def create(self, message: ChatMessage) -> ChatMessage:
        """创建新消息"""
        try:
            query = """
            INSERT INTO chat_messages (id, session_id, role, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.execute(query, (
                message.id,
                message.session_id,
                message.role,
                message.content,
                message.created_at or datetime.now(),
                message.updated_at or datetime.now()
            ))
            self.db.commit()
            return await self.get_by_id(message.id)
        except Exception as e:
            logger.error(f"创建消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建消息失败: {str(e)}")

    async def batch_create(self, messages: List[ChatMessage]):
        """批量创建消息"""
        try:
            query = """
            INSERT INTO chat_messages (id, session_id, role, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.executemany(query, [(
                message.id,
                message.session_id,
                message.role,
                message.content,
                message.created_at or datetime.now(),
                message.updated_at or datetime.now()
            ) for message in messages])
            self.db.commit()
        except Exception as e:
            logger.error(f"批量创建消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"批量创建消息失败: {str(e)}")
    
    async def get_by_id(self, message_id: str) -> Optional[ChatMessage]:
        """获取指定消息"""
        try:
            query = "SELECT * FROM chat_messages WHERE id = ?"
            cursor = self.db.execute(query, (message_id,))
            row = cursor.fetchone()
            if row:
                return ChatMessage.from_dict(dict(row))
            return None
        except Exception as e:
            logger.error(f"获取消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取消息失败: {str(e)}")
    
    async def update(self, message: ChatMessage) -> Optional[ChatMessage]:
        """更新消息"""
        try:
            query = """
            UPDATE chat_messages
            SET content = ?, updated_at = ?
            WHERE id = ?
            """
            self.db.execute(query, (
                message.content,
                message.updated_at or datetime.now(),
                message.id
            ))
            self.db.commit()
            return await self.get_by_id(message.id)
        except Exception as e:
            logger.error(f"更新消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"更新消息失败: {str(e)}")
    
    async def list_by_session(self, session_id: str) -> List[ChatMessage]:
        """获取会话的所有消息"""
        try:
            query = "SELECT * FROM chat_messages WHERE session_id = ? ORDER BY created_at ASC"
            cursor = self.db.execute(query, (session_id,))
            return [ChatMessage.from_dict(dict(row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取会话消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取会话消息失败: {str(e)}")