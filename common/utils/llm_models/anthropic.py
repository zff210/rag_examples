from typing import Dict, Any, List, Tuple, Generator, Union
import anthropic

from .base import BaseLLM

class AnthropicLLM(BaseLLM):
    """Anthropic模型实现"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name', 'claude-3-opus-20240229')
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def load_model(self):
        """Anthropic不需要显式加载模型"""
        pass
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        params = {
            'model': kwargs.get('model', self.model_name),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9))
        }
        
        try:
            response = self.client.completions.create(
                prompt=prompt,
                **params
            )
            return response.completion.strip()
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")
    
    def get_embeddings(self, text: str) -> List[float]:
        """获取文本嵌入"""
        # TODO: 实现文本嵌入
        raise NotImplementedError("Anthropic embeddings not implemented yet")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Generator[str, None, None]]:
        """对话接口"""
        params = {
            'model': kwargs.get('model', self.model_name),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9))
        }
        
        # 获取流式输出参数
        stream = kwargs.pop('stream', False)
        params['stream'] = stream
        
        try:
            # 将消息列表转换为Anthropic格式
            prompt = self._format_messages(messages)
            
            if stream:
                return self._stream_chat(prompt, **params)
            else:
                response = self.client.completions.create(
                    prompt=prompt,
                    **params
                )
                return response.completion.strip()
        except Exception as e:
            raise RuntimeError(f"Anthropic chat error: {str(e)}")
    
    def _stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式对话"""
        try:
            response = self.client.completions.create(
                prompt=prompt,
                **kwargs
            )
            
            for chunk in response:
                if chunk.completion:
                    yield chunk.completion
        except Exception as e:
            raise RuntimeError(f"Anthropic stream chat error: {str(e)}")
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """将消息列表格式化为Anthropic格式"""
        formatted = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'user':
                formatted += f"\nHuman: {content}"
            elif role == 'assistant':
                formatted += f"\nAssistant: {content}"
        return formatted + "\nAssistant:" 