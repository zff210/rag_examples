import json
from ekbase.core.models.chat_request import ChatRequest
from ekbase.handler.prompt_handler import PromptHandler
from ekbase.handler.handlerimpl.mcp_handler import MCPHandler
import requests
from ekbase.config import WEB_SEARCH
import logging
from ekbase.core.models.prompt_process_model import PromptProcessModel


logger = logging.getLogger(__name__)

class WebSearchHandler(PromptHandler):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel ):
        super().__init__(chat_request, process_model)

    def get_next_handler(self) -> 'PromptHandler':
        return MCPHandler(self.chat_request)

    async def build_prompt(self) -> str:
        if self.chat_request.web_search:
            prompt = "Web搜索结果：\n" + await self.perform_web_search(self.chat_request.web_search)
        else:
            prompt = ""
        self.process_model.prompt += (prompt + "\n")
        return prompt + "\n" + await self.get_next_handler().build_prompt()

    # Perform web search (optional, retained for flexibility)
    # https://open.bochaai.com/overview
    async def perform_web_search(query: str):
        try:
            api_key = WEB_SEARCH['api_key']
            if not api_key:
                raise RuntimeError("BOCHAAI_SEARCH_API_KEY is not set")
            
            headers = {
                'Content-Type': 'application/json',  # Remove space
                'Authorization': f'Bearer {api_key}'
            }
        
            payload = json.dumps({
                "query": query,
                "freshness": "noLimit",
                "summary": True, 
                "count": WEB_SEARCH['count']
            })

            # 使用搜索API, 参考文档 https://bocha-ai.feishu.cn/wiki/RXEOw02rFiwzGSkd9mUcqoeAnNK
            response = requests.post(WEB_SEARCH['base_url'] + "/web-search", headers=headers, data=payload)
            
            # Check status code before parsing JSON
            if response.status_code != 200:
                return f"搜索失败，状态码: {response.status_code}"
                
            # Only parse JSON if status code is 200
            try:
                json_data = response.json()
                logger.info(f"web search response: {json_data}")
                return str(json_data)
            except json.JSONDecodeError as e:
                return f"搜索结果JSON解析失败: {str(e)}"
                
        except Exception as e:
            logger.error(f"执行网络搜索时出错: {str(e)}", exc_info=True)
            return f"执行网络搜索时出错: {str(e)}"
        
    def get_process_model(self) -> PromptProcessModel:
        return self.process_model
