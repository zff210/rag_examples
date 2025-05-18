from typing import Dict, Any, List, Generator, Union
import os
from openai import OpenAI
import logging

from .base import BaseLLM

logger = logging.getLogger(__name__)

class DoubaoLLM(BaseLLM):
    """豆包大模型实现"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        logger.debug(f"豆包模型初始化开始: {config}")
        
        # 验证必要的配置
        if not config.get('api_key'):
            raise ValueError("豆包模型初始化失败: 缺少 api_key")
        if not config.get('base_url'):
            raise ValueError("豆包模型初始化失败: 缺少 base_url")
            
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name', 'doubao-1-5-thinking-pro-250415')
        self.base_url = config.get('base_url', 'https://ark.cn-beijing.volces.com/api/v3')
        self.client = None
        
        try:
            logger.debug(f"正在初始化豆包客户端，base_url: {self.base_url}")
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            logger.debug(f"豆包模型初始化成功: {self.client}")
        except Exception as e:
            logger.error(f"豆包模型初始化失败: {str(e)}")
            self._cleanup()
            raise RuntimeError(f"豆包模型初始化失败: {str(e)}")
            
    def _cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'client') and self.client is not None:
                self.client = None
        except Exception as e:
            logger.error(f"豆包模型清理失败: {str(e)}")
            
    def __del__(self):
        """析构函数"""
        self._cleanup()
        
    def load_model(self):
        """豆包不需要显式加载模型"""
        pass
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.client:
            raise RuntimeError("豆包客户端未初始化")
            
        params = {
            'model': kwargs.get('model', self.model_name),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9))
        }
        
        try:
            logger.debug(f"豆包生成文本开始，参数: {params}")
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            logger.debug("豆包生成文本成功")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"豆包生成文本失败: {str(e)}")
            raise RuntimeError(f"豆包 API error: {str(e)}")
    
    def get_embeddings(self, text: str) -> List[float]:
        """获取文本嵌入"""
        if not self.client:
            raise RuntimeError("豆包客户端未初始化")
            
        try:
            logger.debug("豆包获取文本嵌入开始")
            response = self.client.embeddings.create(
                input=text,
                model="doubao-embedding"
            )
            logger.debug("豆包获取文本嵌入成功")
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"豆包获取文本嵌入失败: {str(e)}")
            raise RuntimeError(f"豆包 embeddings error: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Generator[str, None, None]]:
        """对话接口"""
        if not self.client:
            raise RuntimeError("豆包客户端未初始化")
            
        params = {
            'model': kwargs.get('model', self.model_name),
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_tokens': kwargs.get('max_tokens', self.config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9)),
            'stream': kwargs.get('stream', False)
        }

        logger.debug(f"豆包对话接口参数: {params}")
        
        try:
            if params['stream']:
                return self._stream_chat(messages, **params)
            else:
                logger.debug("豆包普通对话开始")
                response = self.client.chat.completions.create(
                    messages=messages,
                    **params
                )
                logger.debug("豆包普通对话成功")
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"豆包对话失败: {str(e)}")
            raise RuntimeError(f"豆包 chat error: {str(e)}")
    
    def _stream_chat(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """流式对话"""
        if not self.client:
            raise RuntimeError("豆包客户端未初始化")
            
        try:
            logger.debug("豆包流式对话开始")
            response = self.client.chat.completions.create(
                messages=messages,
                **kwargs
            )
            
            for chunk in response:
                if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            logger.debug("豆包流式对话完成")
        except Exception as e:
            logger.error(f"豆包流式对话失败: {str(e)}")
            raise RuntimeError(f"豆包 stream chat error: {str(e)}") 