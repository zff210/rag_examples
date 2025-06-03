from ekbase.core.models.chat_request import ChatRequest
from ekbase.handler.prompt_handler import PromptHandler
from ekbase.handler.handlerimpl.web_search_handler import WebSearchHandler
from ekbase.core.models.prompt_process_model import PromptProcessModel

class VectorHandler(PromptHandler):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel):
        super().__init__(chat_request, process_model)

    def get_next_handler(self) -> 'PromptHandler':
        return WebSearchHandler(self.chat_request)

    def get_prompt(self) -> str:
        # TODO: 从向量数据库中获取上下文
        if self.chat_request.vector_db:
            prompt = f"向量数据库中的上下文信息：\n未获取到上下文\n\n"
        else:
            prompt = ""
        self.process_model.prompt += (prompt + "\n")
        return prompt + self.get_next_handler().get_prompt()
    
    def get_process_model(self) -> PromptProcessModel:
        return self.process_model