import os
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
from pathlib import Path
import json
from ekbase.config import STORAGE

class VectorUtils:
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
        self.model = SentenceTransformer(model_name, device=device)

        # 如果index_path和metadata_path为None,则使用默认路径
        if not index_path:
            index_path = os.path.join(STORAGE['vector_index'], 'vector_index.faiss')
        if not metadata_path:
            metadata_path = os.path.join(STORAGE['vector_index'], 'metadata.json')
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.metadata = {}
        self._load_or_create_index()
        
    def _load_or_create_index(self):
        """加载或创建FAISS索引"""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = {}
            
    def _save_index(self):
        """保存索引和元数据"""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            
    def process_file(self, file_path: str, chunk_size: int = 1000) -> None:
        """
        处理文件并存储到向量数据库
        
        Args:
            file_path: 文件路径
            chunk_size: 文本分块大小
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 简单的文本分块
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        # 生成向量
        embeddings = self.model.encode(chunks)
        
        # 添加到索引
        self.index.add(np.array(embeddings).astype('float32'))
        
        # 更新元数据
        start_idx = len(self.metadata)
        for i, chunk in enumerate(chunks):
            self.metadata[str(start_idx + i)] = {
                "file_path": file_path,
                "chunk": chunk,
                "chunk_index": i
            }
            
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
        # 生成查询向量
        query_vector = self.model.encode([query])
        
        # 搜索最相似的向量
        distances, indices = self.index.search(
            np.array(query_vector).astype('float32'),
            top_k
        )
        
        # 整理结果
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if str(idx) in self.metadata:
                result = self.metadata[str(idx)].copy()
                result["similarity_score"] = float(1 / (1 + distance))  # 转换为相似度分数
                results.append(result)
                
        return results 