import sqlite3
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from ekbase.config import settings
import os

logger = logging.getLogger(__name__)

class Database:
    _instance: Optional['Database'] = None
    _conn: Optional[sqlite3.Connection] = None
    _db_path: Optional[str] = None
    

    def __new__(cls):
        """
        单例模式，确保数据库连接唯一\n
        默认使用配置文件中的数据库路径，可通过configure方法配置
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        cls._db_path = settings.DATABASE['path']
        return cls._instance
    
    @classmethod
    def configure(cls, db_path: str):
        """配置数据库文件路径
        
        Args:
            db_path: 数据库文件路径，可以是相对路径或绝对路径
        """
        cls._db_path = db_path
    
    def __init__(self):
        if self._conn is None:
            if self._db_path is None:
                # 默认路径
                self._db_path = settings.DATABASE['path']
            else:
                # 确保路径是绝对路径
                self._db_path = settings.DATABASE['path']
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
    
    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn
    
    @property
    def db_path(self) -> str:
        """获取当前数据库文件路径"""
        return self._db_path
    
    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        cursor = self._conn.cursor()
        cursor.execute(query, params)
        return cursor
    
    def commit(self):
        self._conn.commit()
    
    def rollback(self):
        self._conn.rollback()
    
    def _init_db(self):
        """初始化数据库连接和表结构"""
        try:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            
            # 创建会话表
            self.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
            """)
            
            # 创建消息表
            self.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (id)
            )
            """)
            
            self.commit()
        except Exception as e:
            logger.error(f"初始化数据库失败: {str(e)}", exc_info=True)
            raise RuntimeError(f"初始化数据库失败: {str(e)}")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        try:
            if not self._conn:
                self._conn = sqlite3.connect(self.db_path)
                self._conn.row_factory = sqlite3.Row
            yield self._conn
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