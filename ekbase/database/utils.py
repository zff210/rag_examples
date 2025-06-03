import sqlite3
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from ekbase.config import settings
import os
import uuid
import threading

logger = logging.getLogger(__name__)

class Database:
    _instance: Optional['Database'] = None
    _instances: Dict[str, 'Database'] = {}  # 存储多实例的字典，key为实例ID
    _db_path: Optional[str] = None
    _local = threading.local()  # 线程本地存储
    
    def __new__(cls, db_path: Optional[str] = None, use_singleton: bool = True):
        """
        支持单例和多实例模式
        
        Args:
            db_path: 数据库文件路径，如果为None则使用默认路径
            use_singleton: 是否使用单例模式，默认为True
        """
        if use_singleton:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._instance_id = "singleton"
            return cls._instance
        else:
            instance = super(Database, cls).__new__(cls)
            instance._instance_id = str(uuid.uuid4())  # 生成唯一标识符
            cls._instances[instance._instance_id] = instance
            return instance
    
    @classmethod
    def configure(cls, db_path: str):
        """配置默认数据库文件路径
        
        Args:
            db_path: 数据库文件路径，可以是相对路径或绝对路径
        """
        cls._db_path = db_path
    
    def __init__(self, db_path: Optional[str] = None, use_singleton: bool = True):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径，如果为None则使用默认路径
            use_singleton: 是否使用单例模式，默认为True
        """
        self._instance_id = getattr(self, '_instance_id', None)  # 获取实例ID
        
        if db_path is None:
            # 使用默认路径
            self._db_path = settings.DATABASE['path']
        else:
            # 使用指定路径
            self._db_path = db_path
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
    
    @property
    def connection(self) -> sqlite3.Connection:
        """获取当前线程的数据库连接"""
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self._db_path)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    @property
    def db_path(self) -> str:
        """获取当前数据库文件路径"""
        return self._db_path
    
    @property
    def instance_id(self) -> str:
        """获取实例唯一标识符"""
        return self._instance_id
    
    def close(self):
        """关闭当前线程的数据库连接"""
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
            delattr(self._local, 'conn')
            # 如果是多实例模式，从实例字典中移除
            if self._instance_id in self._instances:
                del self._instances[self._instance_id]
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor
    
    def commit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        try:
            conn = self.connection
            yield conn
        except Exception as e:
            logger.error(f"获取数据库连接失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"获取数据库连接失败: {str(e)}")
    
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """批量执行SQL查询"""
        try:
            with self.get_connection() as conn:
                return conn.executemany(query, params_list)
        except Exception as e:
            logger.error(f"批量执行SQL查询失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"批量执行SQL查询失败: {str(e)}")
    
    def __del__(self):
        """析构函数，确保关闭数据库连接"""
        self.close() 