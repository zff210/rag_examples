from fastapi import APIRouter
from ekbase.api.v1.chat_session_api import router as chat_session_router
from ekbase.api.pub import router as pub_router
from ekbase.api.v1.document_api import router as document_router
from ekbase.api.v1.mcp_api import router as mcp_router

# 创建v1版本的路由
v1_router = APIRouter(prefix="/v1")

# 注册v1版本的所有路由
v1_router.include_router(chat_session_router)
v1_router.include_router(pub_router)
v1_router.include_router(document_router)
v1_router.include_router(mcp_router)