import sqlite3
from typing import Optional
import os
from ekbase.config import settings
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
                self._db_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), 
                    'storage', 
                    'database.db'
                )
            else:
                # 确保路径是绝对路径
                self._db_path = os.path.abspath(self._db_path)
            
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