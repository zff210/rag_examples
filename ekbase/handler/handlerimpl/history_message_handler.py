from ekbase.core.models.chat_request import ChatRequest
from ekbase.handler.prompt_handler import PromptHandler
from ekbase.handler.handlerimpl.vector_handler import VectorHandler
from ekbase.database.services.chat_message_service import ChatMessageService
from ekbase.core.models.prompt_process_model import PromptProcessModel

class HistoryMessageHandler(PromptHandler):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel):
        super().__init__(chat_request, process_model)
        self.message_service = ChatMessageService()

    def get_next_handler(self) -> 'PromptHandler':
        return VectorHandler(self.chat_request, self.process_model)

    async def build_prompt(self) -> str:
        # 获取历史消息
        messages = await self.message_service.list_by_session(self.chat_request.session_id)
        # 构建提示词
        prompt = "上下文信息如下：\n"
        
        if messages:
            prompt += "历史对话：\n"
            for msg in messages:
                prompt += f"{msg.role}: {msg.content}\n"
            prompt += "\n"
            self.process_model.prompt += (prompt + "\n")
        return prompt + await self.get_next_handler().build_prompt()
    
    def get_process_model(self) -> PromptProcessModel:
        return self.process_model