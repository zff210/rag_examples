from ekbase.core.models.chat_request import ChatRequest
from ekbase.handler.prompt_handler import PromptHandler
from ekbase.handler.handlerimpl.final_handler import FinalHandler
from ekbase.core.models.prompt_process_model import PromptProcessModel
from ekbase.core.services.mcp_core_service import MCPCoreService
import json
from fastmcp import Client
from fastmcp.client.transports import SSETransport
import logging

logger = logging.getLogger(__name__)

class MCPHandler(PromptHandler):
    def __init__(self, chat_request: ChatRequest, process_model: PromptProcessModel):
        super().__init__(chat_request, process_model)
        self.mcp_core_service = MCPCoreService()

    def get_next_handler(self) -> 'PromptHandler':
        return FinalHandler(self.chat_request)

    async def build_prompt(self) -> str:
        if self.chat_request.mcp:
            tools = self.mcp_core_service.get_all_tools()
            # Construct tool descriptions for the LLM
            tool_descriptions = "\n".join([
                f"server_url: {tool['url']}\n\ntool_name: {tool['name']}\nDescription: {tool['description']}\ninput_schema: {tool['input_schema']}"
                    for tool in tools
                ]) if tools else "无可用工具"
            # Prompt to decide tool invocation
            agent_prompt = f"""
                上下文信息:\n{self.process_model.prompt}\n
                问题: {self.chat_request.query}\n
                可用工具:\n{tool_descriptions}\n
                你是一个智能助手，可以根据用户问题选择合适的工具执行操作。
                如果需要使用工具，请返回以下格式的JSON：
                ```json
                {{
                "server_url": "server_url",
                "tool_name": "tool_name",
                "parameters":{{"param_name1": "param_value1", "param_name2": "param_value2"}}
                }}
                ```
                如果不需要工具，则直接返回最终结果，返回下列格式的json，结果填充到answer字段
                ```json
                {{
                "answer": "回答内容"
                }}
                ```
                """
            # 使用大模型调用工具
            response = await self.mcp_core_service.call_tool(agent_prompt)
            # 解析大模型调用工具的返回结果
            decision_json = json.loads(response)
            
            if "server_url" in decision_json and "tool_name" in decision_json:
                server_url = decision_json["server_url"]
                tool_name = decision_json["tool_name"]
                parameters = decision_json["parameters"]
                try:
                    async with Client(SSETransport(server_url)) as client: 
                        tool_result = await client.call_tool(tool_name, parameters)
                        tool_response = f"工具 {tool_name} 执行结果：{tool_result}"
                        logger.info(f"工具 {tool_name} 执行结果：{tool_result}")
                        
                        # 继续调用大模型
                        prompt = f"mcp上下文信息:\n{tool_response}"
                except Exception as e:
                    logger.error(f"工具 {tool_name} 执行失败：{e}")
                    prompt = f"工具 {tool_name} 执行失败：{e}"
            else:
                # 不需要工具，直接返回结果
                prompt = decision_json["answer"]
                self.process_model.final_result = prompt
                self.process_model.is_end = True
                return prompt
        else:
            prompt = ""
        self.process_model.prompt += f"\n{prompt}"
        return prompt + "\n" + await self.get_next_handler().build_prompt()
    
    def get_process_model(self) -> PromptProcessModel:
        return self.process_model
