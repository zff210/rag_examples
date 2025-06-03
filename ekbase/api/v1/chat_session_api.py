from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import List
from ekbase.database.services.chat_session_service import ChatSessionService
from ekbase.database.models.chat_session import ChatSession
from ekbase.core.services.chat_service import ChatService
from ekbase.core.models.chat_request import ChatRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat_session"])


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(session_id: str):
    """获取指定会话信息"""
    session_service = ChatSessionService()
    session = await session_service.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions", response_model=List[ChatSession])
async def list_sessions():
    """获取所有会话列表"""
    session_service = ChatSessionService()
    return await session_service.list_all()

@router.put("/sessions/{session_id}", response_model=ChatSession)
async def update_session(session_id: str, session: ChatSession):
    """更新会话信息"""
    session_service = ChatSessionService()
    updated_session = await session_service.update(session)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return updated_session

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    session_service = ChatSessionService()
    if not await session_service.delete(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@router.post("/stream")
async def stream_post(request: Request):
    try:
        # 解析请求体中的 JSON 数据
        req_data = await request.json()
        chat_request = ChatRequest(req_data)
        chat_service = ChatService()    
        return await chat_service.process_stream_request(chat_request)
    except Exception as e:
        error_msg = str(e)
        logger.error(f"聊天接口错误: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)
    

# 导出会话为markdown格式下载
@router.get("/export/{session_id}")
async def export_session(session_id: str):
    try:
        session_service = ChatSessionService()
        session = await session_service.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # 构建markdown内容
        markdown_content = f"# 会话历史记录\n\n"
        markdown_content += f"## 会话ID: {session_id}\n\n"
        markdown_content += f"## 会话总结: {session['summary']}\n\n"
        
        for message in session.messages:
            role = message['role']
            content = message['content']
            markdown_content += f"### {role}\n\n{content}\n\n"
        
        return StreamingResponse(
            iter([markdown_content]), 
            media_type="text/markdown", 
            headers={"Content-Disposition": f"attachment; filename=session_{session_id}.md"}
        )
        
    except Exception as e:
        print(f"导出会话失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"导出会话失败: {str(e)}")
