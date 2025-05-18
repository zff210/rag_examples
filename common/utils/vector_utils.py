import os
from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
import json
from ekbase.config import STORAGE
from common.exception import VectorOperationException
import logging
import atexit
import threading
import signal
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)

@contextmanager
def torch_cuda_context():
    """GPU上下文管理器"""
    try:
        yield
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

class VectorUtils:
    _instance = None
    _initialized = False
    _lock = threading.Lock()
    _ref_count = 0
    _cleanup_registered = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(VectorUtils, cls).__new__(cls)
                    # 注册信号处理
                    signal.signal(signal.SIGINT, cls._signal_handler)
                    signal.signal(signal.SIGTERM, cls._signal_handler)
        return cls._instance

    @classmethod
    def _signal_handler(cls, signum, frame):
        """信号处理函数"""
        if cls._instance:
            cls._instance._cleanup()
        raise KeyboardInterrupt()

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        index_path: str = None,
        metadata_path: str = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """
        初始化向量工具类
        
        Args:
            model_name: 使用的sentence-transformer模型名称
            index_path: FAISS索引保存路径, 默认使用STORAGE['vector_index']
            metadata_path: 元数据保存路径, 默认使用STORAGE['vector_index']
            device: 运行设备
        """
        with self._lock:
            if not self._initialized:
                try:
                    # 设置环境变量
                    os.environ["TOKENIZERS_PARALLELISM"] = "false"
                    os.environ["TOKENIZERS_VERBOSITY"] = "error"
                    
                    # 确保存储目录存在
                    os.makedirs(STORAGE['models'], exist_ok=True)
                    os.makedirs(STORAGE['vectors'], exist_ok=True)
                    
                    # 加载模型
                    model_path = os.path.join(STORAGE['models'], model_name)
                    logger.info(f"正在加载模型，路径: {model_path}")
                    
                    with torch_cuda_context():
                        if not os.path.exists(model_path):
                            logger.info(f"模型不存在，开始下载: {model_name}")
                            self.model = SentenceTransformer(model_name, device=device)
                            logger.info("模型下载完成，开始保存")
                            self.model.save(model_path)
                            logger.info("模型保存完成")
                        else:
                            logger.info("使用本地模型文件")
                            self.model = SentenceTransformer(model_path, device=device)
                    
                    logger.info("模型加载成功")

                    # 初始化索引和元数据
                    if not index_path:
                        index_path = os.path.join(STORAGE['vectors'], 'vector_index.faiss')
                    if not metadata_path:
                        metadata_path = os.path.join(STORAGE['vectors'], 'metadata.json')
                    self.index_path = index_path
                    self.metadata_path = metadata_path
                    self.dimension = self.model.get_sentence_embedding_dimension()
                    self.index = None
                    self.metadata = {}
                    self._load_or_create_index()
                    self._initialized = True
                    logger.info("向量工具类初始化完成")
                    
                except Exception as e:
                    logger.error(f"初始化失败: {str(e)}")
                    raise VectorOperationException(f"向量工具类初始化失败: {str(e)}")
            
            self._ref_count += 1
            
            # 只在第一次初始化时注册清理函数
            if not self._cleanup_registered:
                atexit.register(self._cleanup)
                self._cleanup_registered = True

    def _cleanup(self):
        """清理资源"""
        with self._lock:
            self._ref_count -= 1
            if self._ref_count <= 0:
                try:
                    logger.info("开始清理向量工具资源")
                    if hasattr(self, 'model'):
                        with torch_cuda_context():
                            if hasattr(self.model, 'to'):
                                self.model.to('cpu')
                            del self.model
                    if hasattr(self, 'index'):
                        del self.index
                    if hasattr(self, 'metadata'):
                        del self.metadata
                    logger.info("向量工具资源清理完成")
                except Exception as e:
                    logger.error(f"向量工具资源清理失败: {str(e)}")
                finally:
                    self._initialized = False
                    self._instance = None
                    self._cleanup_registered = False

    def __del__(self):
        """析构函数"""
        try:
            self._cleanup()
        except:
            pass

    def _is_other_models_using_gpu(self):
        """检查是否有其他模型正在使用 GPU"""
        try:
            from common.utils.llm_utils import LLMUtils
            llm_utils = LLMUtils()
            return any(hasattr(model, 'model') and hasattr(model.model, 'device') 
                      and model.model.device.type == 'cuda' 
                      for model in llm_utils.models.values())
        except:
            return False

    def _load_or_create_index(self):
        """加载或创建FAISS索引"""
        if os.path.exists(self.index_path):
            logger.debug(f"索引已经存在，加载索引: {self.index_path}")
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            logger.debug(f"索引加载完成，元数据: {self.metadata}")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = {}
            logger.debug(f"索引创建完成，元数据: {self.metadata}")

    def _save_index(self):
        """保存索引和元数据"""
        logger.debug(f"开始保存索引: {self.index_path}")
        faiss.write_index(self.index, self.index_path)
        logger.debug(f"索引保存完成")
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            logger.debug(f"元数据保存完成")

    def process_file(self, file_path: str, chunk_size: int = 1000) -> None:
        """
        处理文件并存储到向量数据库
        
        Args:
            file_path: 文件路径
            chunk_size: 文本分块大小
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        try:
            # 检查文件是否已经处理过
            file_processed = False
            for metadata in self.metadata.values():
                if metadata.get("file_path") == file_path:
                    file_processed = True
                    logger.info(f"文件已处理过，跳过: {file_path}")
                    break
            
            if file_processed:
                return
                
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单的文本分块
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            # 生成向量
            with torch_cuda_context():
                with torch.no_grad():
                    embeddings = self.model.encode(chunks)
            
            # 添加到索引
            self.index.add(np.array(embeddings).astype('float32'))
            
            # 更新元数据
            start_idx = len(self.metadata)
            for i, chunk in enumerate(chunks):
                self.metadata[str(start_idx + i)] = {
                    "file_path": file_path,
                    "chunk": chunk,
                    "chunk_index": i,
                    "processed_at": datetime.now().isoformat()  # 添加处理时间
                }
                
            # 保存更新后的索引和元数据
            self._save_index()
            logger.info(f"文件处理完成: {file_path}")
            
        except Exception as e:
            logger.error(f"处理文件失败: {str(e)}")
            raise VectorOperationException(f"处理文件失败: {str(e)}")

    def delete_file(self, file_path: str, remove_file: bool = True):
        """
        删除文件，并删除索引中的相关向量
        
        Args:
            file_path: 要删除的文件路径
            remove_file: 是否删除文件, 默认删除

        Throws:
            VectorOperationException: 文件在向量库中未找到相关记录时抛出
        """
        if not os.path.exists(file_path):
            return
            
        # 找出所有与该文件相关的向量索引
        indices_to_remove = []
        for idx, metadata in self.metadata.items():
            if metadata["file_path"] == file_path:
                indices_to_remove.append(int(idx))
                
        if not indices_to_remove:
            raise VectorOperationException(f"警告：在向量库中未找到文件 {file_path} 的相关记录")
            
        # 从索引中删除向量
        self.index.remove_ids(np.array(indices_to_remove))
        
        # 从元数据中删除相关记录
        for idx in indices_to_remove:
            del self.metadata[str(idx)]
            
        # 删除实际文件
        if remove_file:
            os.remove(file_path)
        
        # 保存更新后的索引和元数据
        self._save_index()
        
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相似内容
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            包含相似内容的列表，每个元素包含文件路径和内容
        """
        try:
            # 生成查询向量
            with torch_cuda_context():
                with torch.no_grad():
                    query_vector = self.model.encode([query])
            logger.debug(f"查询向量生成完成")
            
            # 搜索最相似的向量
            distances, indices = self.index.search(
                np.array(query_vector).astype('float32'),
                top_k
            )
            logger.debug(f"搜索完成，结果: {distances}, {indices}")

            # 整理结果
            results = []
            for distance, idx in zip(distances[0], indices[0]):
                if str(idx) in self.metadata:
                    result = self.metadata[str(idx)].copy()
                    result["similarity_score"] = float(1 / (1 + distance))
                    results.append(result)
                    
            return results
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            raise VectorOperationException(f"搜索失败: {str(e)}") 
        

    # 删除当前已经创建的所有索引
    def delete_all_indexes(self):
        """
        删除当前已经创建的所有索引
        """
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
            logger.debug(f"索引删除完成")
            if os.path.exists(self.metadata_path):
                os.remove(self.metadata_path)
                logger.debug(f"元数据删除完成")
        else:
            logger.debug(f"索引不存在，无需删除")
