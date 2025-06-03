import uuid
from ekbase.database.utils import Database
from fastapi import UploadFile, HTTPException
import os
from ekbase.config import STORAGE
from datetime import datetime
from ekbase.database.models.document import Document
from ekbase.database.services.document_service import DocumentService
from common.utils.vector_utils import VectorUtils
import logging

logger = logging.getLogger(__name__)

class DocumentCoreService:
    _instance = None
    _document_index = {}
    _vector_utils = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentCoreService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._vector_utils is None:
            self._vector_utils = VectorUtils()

    def load_documents(self):
        try:
            logger.info("开始加载文档")
            document_service = DocumentService()
            documents = document_service.list_all(with_file_path=True)
            
            for document in documents:
                try:
                    logger.info(f"处理文档: {document.id}")
                    self._document_index[document.id] = document
                    
                    # 检查文件是否存在
                    if not os.path.exists(document.file_path):
                        logger.warning(f"文件不存在: {document.file_path}")
                        continue
                        
                    # 处理文件向量化
                    logger.info(f"开始向量化文件: {document.file_path}")
                    self._vector_utils.process_file(document.file_path)
                    logger.info(f"文件向量化完成: {document.file_path}")
                    
                except Exception as e:
                    logger.error(f"处理文档 {document.id} 时出错: {str(e)}")
                    continue
                    
            logger.info("文档加载完成")
            
        except Exception as e:
            logger.error(f"加载文档失败: {str(e)}")
            raise

    @property
    def document_index(self):
        return self._document_index
    
    def reload_index(self):
        """重建索引"""
        self._vector_utils.delete_all_indexes()
        self.load_documents()
    
    def add_document(self, document: Document):
        try:
            logger.info(f"添加文档: {document.id}")
            self._document_index[document.id] = document
            
            # 检查文件是否存在
            if not os.path.exists(document.file_path):
                raise FileNotFoundError(f"文件不存在: {document.file_path}")
                
            # 处理文件向量化
            logger.info(f"开始向量化文件: {document.file_path}")
            self._vector_utils.process_file(document.file_path)
            logger.info(f"文件向量化完成: {document.file_path}")
            
        except Exception as e:
            logger.error(f"添加文档失败: {str(e)}")
            raise

    async def upload_document(self, file: UploadFile):
        """
        上传文档, 并保存到磁盘, 并保存到数据库, 并重建索引
        
        Args:
            file: 上传的文件
            
        Returns:
            Document: 上传的文档
        """
        if not file.filename.endswith((".txt", ".pdf", ".docx")):
            raise HTTPException(status_code=400, detail="仅支持.txt或.pdf或.docx文件")
        
        document_dir = STORAGE['documents']
        # 确保docs目录存在
        os.makedirs(document_dir, exist_ok=True)
        today_str = datetime.now().strftime("%Y%m%d")

        # 判断是否存在以当天日期命名的文件夹
        today_dir = os.path.join(document_dir, today_str)
        os.makedirs(today_dir, exist_ok=True)
        
        file_path = os.path.join(today_dir, file.filename)
        # 检查文件名是否重复，如果重复则添加时间戳
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%H%M%S")
            filename, extension = os.path.splitext(file.filename)
            file_path = os.path.join("docs", f"{filename}_{timestamp}{extension}")
            final_file_name = f"{filename}_{timestamp}{extension}"
        else:
            final_file_name = file.filename
        
        # 读取文件内容
        file_content = file.file.read()
        # 保存文件到磁盘
        logger.debug(f"开始保存文件到磁盘: {file_path}")
        with open(file_path, "wb") as f:
            f.write(file_content)
        logger.debug(f"文件保存完成: {file_path}")
        # 存储文件相关信息到数据库
        document = Document(
            id=str(uuid.uuid4()),
            file_name=final_file_name,
            file_path=file_path,
            created_at=datetime.now()
        )
        document_service = DocumentService()
        document_service.create(document)
        logger.debug(f"文件信息存储到数据库: {document.id}")
        # 更新_document_index
        logger.debug(f"开始更新_document_index: {document.id}")
        self.add_document(document)
        logger.debug(f"_document_index更新完成: {document.id}")

        # 重建索引
        logger.debug(f"开始重建索引: {document.id}")
        self._vector_utils.process_file(file_path)
        logger.debug(f"索引重建完成: {document.id}")
        return document

    def search_document(self, query: str, top_k: int = 5):
        """
        搜索文档

        Args:
            query: 搜索关键词
            top_k: 返回结果数量
            
        Returns:
            List[Document]: 搜索结果
        """
        try:
            logger.debug(f"开始搜索文档: {query}")
            results = self._vector_utils.search(query, top_k)
            return results
        except Exception as e:
            logger.error(f"搜索文档失败: {str(e)}")
            raise

    def delete_document(self, document_id: str):
        """
        删除文档
        """
        document_service = DocumentService()
        try:
            document = document_service.get_by_id(document_id)
            document_service.delete(document_id)
            self._vector_utils.delete_file(document.file_path)
        except Exception as e:
            logger.error(f"删除文件失败: {e}")
            raise e

    def list_documents(self):
        """
        列出所有文档
        """
        document_service = DocumentService()
        return document_service.list_all(with_file_path=False)

    def get_index_status(self):
        """
        获取索引状态
        """
        return self._vector_utils.get_index_status()

    def reset_index(self, document_id: str):
        """
        重置索引
        """
        self._vector_utils.delete_file(document_id, remove_file=False)
        document_service = DocumentService()
        document = document_service.get_by_id(document_id)
        self._vector_utils.process_file(document.file_path)
