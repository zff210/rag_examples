import os
from typing import Dict, Any, List, Tuple, Generator, Union
from transformers import AutoTokenizer, AutoModel
import torch
import gc

from .base import BaseLLM

class ChatGLM(BaseLLM):
    """ChatGLM模型实现"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.model_name = config.get('model_name', 'chatglm3-6b')
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', self.model_name)
        self.model = None
        self.tokenizer = None
        # 设置环境变量，禁用多进程
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        # 设置 CUDA 设备
        if torch.cuda.is_available():
            torch.cuda.set_device(0)  # 使用第一个 GPU
            torch.cuda.empty_cache()  # 清空 GPU 缓存
    
    def load_model(self):
        """加载ChatGLM模型"""
        try:
            # 如果已经加载，先清理
            self._cleanup()
            
            # 加载模型
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                device_map='auto'  # 自动选择设备
            )
            
            self.model = AutoModel.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                device_map='auto',  # 自动选择设备
                torch_dtype=torch.float16  # 使用半精度
            )
            
            # 设置为评估模式
            self.model.eval()
            
        except Exception as e:
            self._cleanup()  # 发生错误时清理资源
            raise RuntimeError(f"Failed to load ChatGLM model: {str(e)}")
    
    def _cleanup(self):
        """清理资源"""
        try:
            if self.model is not None:
                del self.model
            if self.tokenizer is not None:
                del self.tokenizer
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()  # 强制垃圾回收
        except Exception as e:
            print(f"Error cleaning up ChatGLM resources: {str(e)}")
        finally:
            self.model = None
            self.tokenizer = None
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        params = {
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_length': kwargs.get('max_length', self.config.get('max_length', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9))
        }
        
        try:
            with torch.no_grad(), torch.cuda.amp.autocast():  # 使用自动混合精度
                response, _ = self.model.chat(self.tokenizer, prompt, **params)
            return response
        except Exception as e:
            raise RuntimeError(f"ChatGLM generation error: {str(e)}")
    
    def get_embeddings(self, text: str) -> List[float]:
        """获取文本嵌入"""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        # TODO: 实现文本嵌入
        raise NotImplementedError("ChatGLM embeddings not implemented yet")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Generator[str, None, None]]:
        """对话接口"""
        if not self.model or not self.tokenizer:
            self.load_model()
        
        # 将消息列表转换为ChatGLM格式
        prompt = self._format_messages(messages)
        
        # 获取流式输出参数
        stream = kwargs.pop('stream', False)
        
        try:
            if stream:
                return self._stream_chat(prompt, **kwargs)
            else:
                response = self.generate_text(prompt, **kwargs)
                return response
        except Exception as e:
            raise RuntimeError(f"ChatGLM chat error: {str(e)}")
    
    def _stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """流式对话"""
        params = {
            'temperature': kwargs.get('temperature', self.config.get('temperature', 0.7)),
            'max_length': kwargs.get('max_length', self.config.get('max_length', 2048)),
            'top_p': kwargs.get('top_p', self.config.get('top_p', 0.9))
        }
        
        try:
            with torch.no_grad(), torch.cuda.amp.autocast():  # 使用自动混合精度
                for response in self.model.stream_chat(self.tokenizer, prompt, **params):
                    yield response[0]
        except Exception as e:
            raise RuntimeError(f"ChatGLM stream chat error: {str(e)}")
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """将消息列表格式化为ChatGLM格式"""
        formatted = ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'user':
                formatted += f"用户：{content}\n"
            elif role == 'assistant':
                formatted += f"助手：{content}\n"
        return formatted
    
    def __del__(self):
        """析构函数"""
        self._cleanup() 