import uuid
from ekbase.database.utils import Database
from fastapi import UploadFile, HTTPException
import os
from ekbase.config import STORAGE
from datetime import datetime
from ekbase.database.models.document import Document
from ekbase.database.services.document_service import DocumentService
from common.utils.vector_utils import VectorUtils

class DocumentCoreService:
    _instance = None
    _document_index = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DocumentCoreService, cls).__new__(cls)
            # 在创建实例时加载document_index
            if not cls._document_index:
                document_service = DocumentService()
                documents = document_service.get_all()
                for document in documents:
                    cls._document_index[document.id] = document
                    # 初始化向量数据库
                    vector_utils = VectorUtils()
                    vector_utils.process_file(document.file_path)
                
        return cls._instance

    @property
    def document_index(self):
        return self._document_index
    
    def add_document(self, document: Document):
        self._document_index[document.id] = document

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
        # 存储文件相关信息到数据库
        document = Document(
            id=str(uuid.uuid4()),
            file_name=final_file_name,
            file_path=file_path,
            created_at=datetime.now()
        )
        document_service = DocumentService()
        document_service.create(document)
        # 读取文件内容
        file_content = await file.file.read()
        # 保存文件到磁盘
        with open(final_file_name, "wb") as f:
            f.write(file_content)

        # 更新_document_index
        self.add_document(document)

        # 重建索引
        vector_utils = VectorUtils()
        vector_utils.process_file(file_path)

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
        vector_utils = VectorUtils()
        return vector_utils.search(query, top_k)
