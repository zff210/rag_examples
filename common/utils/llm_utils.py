import os
from typing import Optional, Dict, Any, List, Generator, Union
import logging
from functools import wraps
import time
import atexit
import threading
import torch

from common.utils.llm_models import ChatGLM, OpenAILLM, AnthropicLLM, DoubaoLLM

logger = logging.getLogger(__name__)

class LLMUtils:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, config: Optional[Dict[str, Any]] = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_config(config)
                    cls._instance._init_models()
                    # 注册清理函数
                    atexit.register(cls._instance._cleanup)
        return cls._instance
    
    def _cleanup(self):
        """清理资源"""
        try:
            logger.info("开始清理LLM资源")
            if hasattr(self, 'models'):
                for model_name, model in list(self.models.items()):
                    try:
                        # 清理模型资源
                        if hasattr(model, 'model'):
                            del model.model
                        if hasattr(model, 'tokenizer'):
                            del model.tokenizer
                        if hasattr(model, 'client'):
                            del model.client
                        # 清理模型实例
                        del model
                    except Exception as e:
                        logger.error(f"清理模型 {model_name} 失败: {str(e)}")
                self.models.clear()
            # 清理配置
            if hasattr(self, 'config'):
                self.config.clear()
            # 只在没有其他模型使用时清理 GPU 内存
            if torch.cuda.is_available() and not self._is_other_models_using_gpu():
                torch.cuda.empty_cache()
            logger.info("LLM资源清理完成")
        except Exception as e:
            logger.error(f"LLM资源清理失败: {str(e)}")
        finally:
            # 确保实例被清理
            with self._lock:
                self.__class__._instance = None
    
    def _is_other_models_using_gpu(self):
        """检查是否有其他模型正在使用 GPU"""
        try:
            from common.utils.vector_utils import VectorUtils
            vector_utils = VectorUtils()
            return (hasattr(vector_utils, 'model') and 
                   hasattr(vector_utils.model, 'device') and 
                   vector_utils.model.device.type == 'cuda')
        except:
            return False
    
    def _init_config(self, config: Optional[Dict[str, Any]] = None):
        """初始化配置"""
        logger.debug(f"初始化配置: {config}")
        default_config = {
            'model_name': 'doubao-1-5-thinking-pro-250415',
            'api_key': '',  # 添加默认的 api_key
            'temperature': 0.7,
            'max_length': 2048,
            'top_p': 0.9,
            'base_url': 'https://ark.cn-beijing.volces.com/api/v3'
        }
        
        if config is None:
            self.config = default_config
        else:
            # 合并配置，确保所有必要的字段都存在
            self.config = {**default_config, **config}
            
        self.logger = logger
        
        # 设置环境变量，禁用多进程
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        
        # 验证必要的配置
        if not self.config.get('api_key'):
            raise ValueError("LLM初始化失败: 缺少 api_key")
        if not self.config.get('base_url'):
            raise ValueError("LLM初始化失败: 缺少 base_url")
            
    def _init_models(self):
        """初始化模型"""
        logger.debug(f"初始化模型: {self.config['model_name']}")
        self.models = {}
        try:
            self._load_model(self.config['model_name'])
        except Exception as e:
            logger.error(f"模型初始化失败: {str(e)}")
            raise
    
    def _load_model(self, model_name: str):
        """加载指定模型"""
        logger.debug(f"加载模型 开始: {model_name}")
        try:
            # 检查模型是否已经加载
            if model_name in self.models:
                return
                
            # 获取模型类型
            model_type = None
            if model_name.startswith('chatglm'):
                model_type = 'chatglm'
            elif model_name.startswith('gpt'):
                model_type = 'gpt'
            elif model_name.startswith('claude'):
                model_type = 'claude'
            elif model_name.startswith('doubao'):
                model_type = 'doubao'
            else:
                raise ValueError(f"Unsupported model: {model_name}")
            
            # 检查是否已存在同类型模型实例
            for existing_model_name, existing_model in self.models.items():
                if existing_model_name.startswith(model_type):
                    logger.info(f"复用已存在的{model_type}模型实例: {existing_model_name}")
                    self.models[model_name] = existing_model
                    return
            
            # 创建新的模型实例
            if model_type == 'chatglm':
                self.models[model_name] = ChatGLM(self.config)
            elif model_type == 'gpt':
                self.models[model_name] = OpenAILLM(self.config)
            elif model_type == 'claude':
                self.models[model_name] = AnthropicLLM(self.config)
            elif model_type == 'doubao':
                logger.debug(f"加载doubao模型开始: {model_name}")
                self.models[model_name] = DoubaoLLM(self.config)
                logger.debug(f"加载doubao模型成功: {self.models[model_name]}")
            
            self.models[model_name].load_model()
        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {str(e)}")
            raise
    
    def retry_on_error(max_retries: int = 3, delay: int = 1):
        """重试装饰器"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if i == max_retries - 1:
                            raise
                        logger.warning(f"Retry {i+1}/{max_retries} due to error: {str(e)}")
                        time.sleep(delay)
                return None
            return wrapper
        return decorator
    
    @retry_on_error()
    def generate_text(self, prompt: str, model_name: Optional[str] = None, **kwargs) -> str:
        """生成文本"""
        model_name = model_name or self.config['model_name']
        if model_name not in self.models:
            self._load_model(model_name)
        
        return self.models[model_name].generate_text(prompt, **kwargs)
    
    @retry_on_error()
    def get_embeddings(self, text: str, model_name: Optional[str] = None) -> List[float]:
        """获取文本嵌入"""
        model_name = model_name or self.config['model_name']
        if model_name not in self.models:
            self._load_model(model_name)
        
        return self.models[model_name].get_embeddings(text)
    
    @retry_on_error()
    def chat(self, messages: List[Dict[str, str]], model_name: Optional[str] = None, **kwargs) -> Union[str, Generator[str, None, None]]:
        """对话接口
        
        Args:
            messages: 消息列表
            model_name: 模型名称
            stream: 是否使用流式输出
            **kwargs: 其他参数
            
        Returns:
            如果stream=True，返回生成器，否则返回完整响应
        """
        model_name = model_name or self.config['model_name']
        if model_name not in self.models:
            self._load_model(model_name)
        
        return self.models[model_name].chat(messages, **kwargs)
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                # 更新所有已加载模型的配置
                for model in self.models.values():
                    model.update_config(**{key: value})
    
    def set_config(self, config: Dict[str, Any]):
        """设置新的配置"""
        self.config = config
        # 清空已加载的模型
        self.models.clear()
        # 重新加载默认模型
        self._load_model(self.config['model_name']) 