from typing import List, Optional
from datetime import datetime
from ekbase.database.utils import Database
from ekbase.database.models.chat_session import ChatSession
from ekbase.database.services.chat_message_service import ChatMessageService

class ChatSessionService:
    def __init__(self):
        self.db = Database()
    
    def create(self, session: ChatSession) -> ChatSession:
        query = """
        INSERT INTO chat_sessions (id, summary, created_at, updated_at)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(query, (
            session.id,
            session.summary,
            datetime.now(),
            datetime.now()
        ))
        self.db.commit()
        return self.get_by_id(session.id)
    
    def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        query = "SELECT * FROM chat_sessions WHERE id = ?"
        cursor = self.db.execute(query, (session_id,))
        row = cursor.fetchone()
        if row:
            message_service = ChatMessageService()
            messages = message_service.list_by_session(session_id)
            return ChatSession.from_dict(dict(row), messages)
        return None
    
    def update(self, session: ChatSession) -> Optional[ChatSession]:
        query = """
        UPDATE chat_sessions
        SET summary = ?, updated_at = ?
        WHERE id = ?
        """
        self.db.execute(query, (
            session.summary,
            datetime.now(),
            session.id
        ))
        self.db.commit()
        return self.get_by_id(session.id)
    
    def delete(self, session_id: str) -> bool:
        query = "DELETE FROM chat_sessions WHERE id = ?"
        self.db.execute(query, (session_id,))
        self.db.commit()
        return True
    
    def list_all(self) -> List[ChatSession]:
        query = "SELECT * FROM chat_sessions ORDER BY created_at DESC"
        cursor = self.db.execute(query)
        return [ChatSession.from_dict(dict(row)) for row in cursor.fetchall()] 