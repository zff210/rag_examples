from abc import ABC, abstractmethod
from ekbase.core.models.chat_request import ChatRequest
from ekbase.core.models.prompt_process_model import PromptProcessModel

class PromptHandler(ABC):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel):
        self.chat_request = chat_request
        if process_model:
            process_model.is_end = False 
            process_model.prompt = ""
        self.process_model = process_model

    @abstractmethod
    def get_next_handler(self) -> 'PromptHandler':
        """
        获取下一个处理器
        """
        pass

    @abstractmethod
    async def build_prompt(self) -> str:
        """
        构建提示词
        如果启用了mcp，则会根据大模型的调用结果判断是否需要继续请求，如果需要则使用该方法返回的prompt继续请求大模型，否则直接返回用户结果即可
        """
        pass

    @abstractmethod
    def get_process_model(self) -> PromptProcessModel:
        """
        获取处理结果
        """
        pass
