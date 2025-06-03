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

# MCP配置
MCP = {
    # 请求大模型工具数量限制
    'limit': 50
}

# 服务配置
SERVER = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': False,
    'reload_dirs': []
}

# 搜索配置
WEB_SEARCH = {
    'api_key': os.getenv("BOCHAAI_SEARCH_API_KEY"),
    'base_url': "https://api.bochaai.com/v1",
    'count': 10
}   

# 日志配置
LOGGING = {
    # 日志文件存储位置
    'log_dir': os.path.join(BASE_DIR, 'logs'),
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s'
        }
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
        },
        'common.utils.vector_utils': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'ekbase.core.services.document_service': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# 文件存储配置
STORAGE = {
    'documents': os.path.join(BASE_DIR, 'storage', 'documents'),
    'vectors': os.path.join(BASE_DIR, 'storage', 'vectors'),
    'temp': os.path.join(BASE_DIR, 'storage', 'temp'),
    'models': os.path.join(BASE_DIR, 'storage', 'models')
}

# 向量数据库配置
VECTOR_DB = {
    'dimension': 768,  # 向量维度
    'index_type': 'IVFFlat',  # 索引类型
    'nlist': 100,  # 聚类中心数量
}

# 大模型配置
LLM = {
    'model_name': 'doubao-1-5-thinking-pro-250415',
    'temperature': 0.7,
    'max_length': 2048,
    'top_p': 0.9,
    'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
    'api_key': os.getenv("OPENAI_API_KEY")
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