from typing import Dict, Any, List, Tuple, Generator, Union
import openai

from .base import BaseLLM

class OpenAILLM(BaseLLM):
    """OpenAI模型实现"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name', 'gpt-3.5-turbo')
        openai.api_key = self.api_key
    
    def load_model(self):
        """OpenAI不需要显式加载模型"""
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
            response = openai.Completion.create(
                prompt=prompt,
                **params
            )
            return response.choices[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def get_embeddings(self, text: str) -> List[float]:
        """获取文本嵌入"""
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            raise RuntimeError(f"OpenAI embeddings error: {str(e)}")
    
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
            if stream:
                return self._stream_chat(messages, **params)
            else:
                response = openai.ChatCompletion.create(
                    messages=messages,
                    **params
                )
                return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI chat error: {str(e)}")
    
    def _stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """流式对话"""
        try:
            response = openai.ChatCompletion.create(
                messages=messages,
                **kwargs
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise RuntimeError(f"OpenAI stream chat error: {str(e)}") 