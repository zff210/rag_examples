from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple, Generator, Union

class BaseLLM(ABC):
    """大模型基类，定义所有模型必须实现的接口"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.tokenizer = None
    
    @abstractmethod
    def load_model(self):
        """加载模型"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    @abstractmethod
    def get_embeddings(self, text: str) -> List[float]:
        """获取文本嵌入"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Union[str, Generator[str, None, None]]:
        """对话接口
        
        Args:
            messages: 消息列表
            stream: 是否使用流式输出
            **kwargs: 其他参数
            
        Returns:
            如果stream=True，返回生成器，否则返回完整响应
        """
        pass
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value 