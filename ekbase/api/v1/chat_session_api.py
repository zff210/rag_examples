from fastapi import APIRouter, HTTPException
from typing import List
from ekbase.database.services.chat_session_service import ChatSessionService
from ekbase.database.models.chat_session import ChatSession

router = APIRouter(prefix="/chat_session", tags=["chat_session"])


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(session_id: str):
    """获取指定会话信息"""
    session_service = ChatSessionService()
    session = session_service.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions", response_model=List[ChatSession])
async def list_sessions():
    """获取所有会话列表"""
    session_service = ChatSessionService()
    return session_service.list_all()

@router.put("/sessions/{session_id}", response_model=ChatSession)
async def update_session(session_id: str, session: ChatSession):
    """更新会话信息"""
    session_service = ChatSessionService()
    updated_session = session_service.update(session)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return updated_session

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    session_service = ChatSessionService()
    if not session_service.delete(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}