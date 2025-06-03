from ekbase.core.models.chat_request import ChatRequest
from ekbase.handler.prompt_handler import PromptHandler
from ekbase.core.models.prompt_process_model import PromptProcessModel

class FinalHandler(PromptHandler):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel):
        super().__init__(chat_request, process_model)

    def get_next_handler(self) -> 'PromptHandler':
        return None

    async def build_prompt(self) -> str:
        return f"用户问题：{self.chat_request.query}"
    
    def get_process_model(self) -> PromptProcessModel:
        return self.process_model