import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据库配置
DATABASE = {
    'path': os.path.join(BASE_DIR, 'data', 'database.db'),
    'pool_size': 5,
    'max_overflow': 10,
    'echo': False
}

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# 文件存储配置
STORAGE = {
    'documents': os.path.join(BASE_DIR, 'storage', 'documents'),
    'vectors': os.path.join(BASE_DIR, 'storage', 'vectors'),
    'temp': os.path.join(BASE_DIR, 'storage', 'temp'),
}

# 向量数据库配置
VECTOR_DB = {
    'dimension': 768,  # 向量维度
    'index_type': 'IVFFlat',  # 索引类型
    'nlist': 100,  # 聚类中心数量
}

# 大模型配置
LLM = {
    'model_name': 'chatglm3-6b',
    'temperature': 0.7,
    'max_length': 2048,
    'top_p': 0.9,
}

# 安全配置
SECURITY = {
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key-here'),
    'token_expire_minutes': 60 * 24,  # 24小时
    'algorithm': 'HS256',
}

# 缓存配置
CACHE = {
    'type': 'redis',
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'expire': 3600,  # 1小时
}

# 跨域配置
CORS = {
    'origins': ['*'],
    'methods': ['*'],
    'headers': ['*'],
}

# 分页配置
PAGINATION = {
    'default_page_size': 10,
    'max_page_size': 100,
} 