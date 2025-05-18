from .settings import *

# 开发环境特定配置

# 调试模式
DEBUG = True

# 数据库配置
DATABASE.update({
    'echo': True,  # 显示SQL语句
})

# 日志配置
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['handlers']['file']['level'] = 'DEBUG'
LOGGING['loggers']['']['level'] = 'DEBUG'

# 缓存配置
CACHE.update({
    'type': 'memory',  # 开发环境使用内存缓存
    'expire': 300,  # 5分钟
})

# 跨域配置
CORS.update({
    'origins': ['http://localhost:3000', 'http://127.0.0.1:3000'],
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'headers': ['Content-Type', 'Authorization'],
})

# 测试配置
TESTING = {
    'database': {
        'path': ':memory:',  # 使用内存数据库进行测试
    },
    'mock_llm': True,  # 使用模拟的LLM响应
    'mock_vector_db': True,  # 使用模拟的向量数据库
} 