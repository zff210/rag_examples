from typing import List, Optional
from datetime import datetime
from ekbase.config import settings
from ekbase.database.utils import Database
from ekbase.database.models.chat_message import ChatMessage

class ChatMessageService:
    def __init__(self):
        self.db = Database()
    
    def create(self, message: ChatMessage) -> ChatMessage:
        query = """
        INSERT INTO chat_messages (id, session_id, role, content, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, (
            message.id,
            message.session_id,
            message.role,
            message.content,
            datetime.now(),
            datetime.now()
        ))
        self.db.commit()
        return self.get_by_id(message.id)
    
    def get_by_id(self, message_id: str) -> Optional[ChatMessage]:
        query = "SELECT * FROM chat_messages WHERE id = ?"
        cursor = self.db.execute(query, (message_id,))
        row = cursor.fetchone()
        if row:
            return ChatMessage.from_dict(dict(row))
        return None
    
    def update(self, message: ChatMessage) -> Optional[ChatMessage]:
        query = """
        UPDATE chat_messages
        SET content = ?, updated_at = ?
        WHERE id = ?
        """
        self.db.execute(query, (
            message.content,
            datetime.now(),
            message.id
        ))
        self.db.commit()
        return self.get_by_id(message.id)
    
    def delete(self, message_id: str) -> bool:
        query = "DELETE FROM chat_messages WHERE id = ?"
        self.db.execute(query, (message_id,))
        self.db.commit()
        return True
    
    def list_by_session(self, session_id: str) -> List[ChatMessage]:
        query = "SELECT * FROM chat_messages WHERE session_id = ? ORDER BY created_at ASC"
        cursor = self.db.execute(query, (session_id,))
        return [ChatMessage.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def list_all(self) -> List[ChatMessage]:
        query = "SELECT * FROM chat_messages ORDER BY created_at DESC"
        cursor = self.db.execute(query)
        return [ChatMessage.from_dict(dict(row)) for row in cursor.fetchall()] 