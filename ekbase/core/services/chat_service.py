import asyncio
import json
from ekbase.core.models.chat_request import ChatRequest
from ekbase.core.models.prompt_process_model import PromptProcessModel
from ekbase.handler.handlerimpl.history_message_handler import HistoryMessageHandler
from fastapi.responses import StreamingResponse
from ekbase.database.services.chat_session_service import ChatSessionService
from ekbase.database.services.chat_message_service import ChatMessageService
from ekbase.database.models.chat_message import ChatMessage
from ekbase.database.models.chat_session import ChatSession
from datetime import datetime
import uuid
from ekbase.core.services.document_core_service import DocumentCoreService
import logging
from ekbase.config import LLM
from common.utils.llm_utils import LLMUtils
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.session_service = ChatSessionService()
        self.message_service = ChatMessageService()
        config = LLM
        # 从环境变量取apikey
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            config['api_key'] = api_key
        self.llm = LLMUtils(config)
    
    async def process_stream_request(self, chat_request: ChatRequest):
        """处理聊天请求"""
        try:
            # 获取或创建会话
            session_id = chat_request.session_id
            session = None
            if not session_id:
                session_id = str(uuid.uuid4())
            else:   
                session = await self.session_service.get_by_id(session_id)
                if not session:
                    raise RuntimeError("会话不存在")
            has_session = session is not None
            
            # 构建提示词
            process_model = PromptProcessModel()
            prompt_handler = HistoryMessageHandler(chat_request, process_model)
            prompt = await prompt_handler.build_prompt()

            # 如果已经结束，则直接返回结果
            if process_model.is_end:
                # 响应完成后，将完整会话保存到数据库
                if has_session:
                    await self.add_message_to_session(session_id, chat_request.query, process_model.final_result)
                else:
                    await self.create_new_chat_session(session_id, chat_request.query, process_model.final_result)

                return StreamingResponse(
                    generate(initial_content=process_model.final_result),
                    media_type="text/event-stream",
                    headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "Transfer-Encoding": "chunked"}
                )
            
            # 用于保存完整响应
            full_response = ""
            
            # 创建stream响应    
            async def generate():
                nonlocal full_response
                try:
                    # 调用llm的流式输出方法
                    stream_response = self.llm.chat(
                        messages=[
                            # {"role": "system", "content": "你是一个专业的问答助手。请仅基于提供的上下文信息回答问题，不要添加任何未在上下文中提及的信息。如果没有相关信息，请明确告知用户无法回答该问题。"},
                            {"role": "system", "content": "你是一个专业的问答助手。请优先基于提供的上下文信息回答问题，如果上下文信息不足，请根据用户的问题给出回答。"},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True
                    )
                    
                    if stream_response is None:
                        raise RuntimeError("流式响应为空")
                    
                    # 使用同步迭代器处理流式响应
                    for chunk in stream_response:
                        if chunk:  # 确保chunk不为None
                            full_response += chunk
                            yield f"{json.dumps({'content': chunk, 'session_id': session_id})}\n\n"
                            await asyncio.sleep(0.01)  # 添加小延迟确保流式输出
                    
                    # 流式输出完成
                    yield f"{json.dumps({'content': '', 'session_id': session_id, 'done': True})}\n\n"
                    
                    # 响应完成后，将完整会话保存到数据库
                    if has_session:
                        await self.add_message_to_session(session_id, chat_request.query, full_response)
                    else:
                        await self.create_new_chat_session(session_id, chat_request.query, full_response)
                        
                except Exception as e:
                    logger.error(f"流式处理失败: {str(e)}", exc_info=True)
                    error_msg = f"处理请求时发生错误: {str(e)}"
                    yield f"data: {json.dumps({'content': error_msg, 'session_id': session_id, 'error': True})}\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Transfer-Encoding": "chunked"
                }
            )
            
        except Exception as e:
            logger.error(f"处理聊天请求失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"处理聊天请求失败: {str(e)}")
    
    async def create_new_chat_session(self, session_id: str, query: str, response: str):
        """创建新的聊天会话"""
        try:
            # 创建会话
            session = ChatSession(
                id=session_id,
                summary=query[:50] + "..." if len(query) > 50 else query
            )
            await self.session_service.create(session)
            
            # 创建用户消息
            user_message = ChatMessage(
                id=f"{session_id}_user_{datetime.now().timestamp()}",
                session_id=session_id,
                role="user",
                content=query
            )
            # 创建助手消息
            assistant_message = ChatMessage(
                id=f"{session_id}_assistant_{datetime.now().timestamp()}",
                session_id=session_id,
                role="assistant",
                content=response
            )
            await self.message_service.batch_create([user_message, assistant_message])
            
        except Exception as e:
            logger.error(f"创建新聊天会话失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"创建新聊天会话失败: {str(e)}")
    
    async def add_message_to_session(self, session_id: str, query: str, response: str):
        """向现有会话添加消息"""
        try:
            # 创建用户消息
            user_message = ChatMessage(
                id=f"{session_id}_user_{datetime.now().timestamp()}",
                session_id=session_id,
                role="user",
                content=query
            )
            # 创建助手消息
            assistant_message = ChatMessage(
                id=f"{session_id}_assistant_{datetime.now().timestamp()}",
                session_id=session_id,
                role="assistant",
                content=response
            )
            # 创建助手消息
            assistant_message = ChatMessage(
                id=f"{session_id}_assistant_{datetime.now().timestamp()}",
                session_id=session_id,
                role="assistant",
                content=response
            )
            await self.message_service.batch_create([user_message, assistant_message])
            
            # 更新会话时间戳
            session = await self.session_service.get_by_id(session_id)
            if session:
                session.updated_at = datetime.now()
                await self.session_service.update(session)
            
        except Exception as e:
            logger.error(f"向会话添加消息失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"向会话添加消息失败: {str(e)}")