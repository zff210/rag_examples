from .settings import *

# 生产环境特定配置

# 调试模式
DEBUG = False

# 数据库配置
DATABASE.update({
    'echo': False,  # 生产环境不显示SQL语句
    'pool_size': 20,  # 更大的连接池
    'max_overflow': 30,  # 更多的溢出连接
})

# 日志配置
LOGGING.update({
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'WARNING',  # 生产环境只显示警告和错误
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',  # 使用轮转文件处理器
            'formatter': 'standard',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,  # 保留10个备份文件
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
})

# 大模型配置
LLM.update({
    'model_name': 'chatglm3-6b',  # 生产环境使用稳定版本
    'temperature': 0.5,  # 生产环境使用更低的温度值，使输出更稳定
    'max_length': 2048,  # 生产环境使用标准上下文长度
})

# 缓存配置
CACHE.update({
    'type': 'redis',
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'password': os.getenv('REDIS_PASSWORD', None),
    'expire': 3600,  # 1小时
})

# 跨域配置
CORS.update({
    'origins': os.getenv('ALLOWED_ORIGINS', '').split(','),  # 从环境变量读取允许的源
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'headers': ['Content-Type', 'Authorization'],
})

# 安全配置
SECURITY.update({
    'secret_key': os.getenv('SECRET_KEY'),  # 必须从环境变量读取密钥
    'token_expire_minutes': 60 * 24,  # 24小时
    'algorithm': 'HS256',
})

# 性能配置
PERFORMANCE = {
    'worker_count': int(os.getenv('WORKER_COUNT', 4)),  # 工作进程数
    'thread_count': int(os.getenv('THREAD_COUNT', 8)),  # 线程数
    'timeout': 30,  # 请求超时时间（秒）
}

# 监控配置
MONITORING = {
    'enabled': True,
    'metrics_port': int(os.getenv('METRICS_PORT', 9090)),
    'health_check_interval': 30,  # 健康检查间隔（秒）
}

# 备份配置
BACKUP = {
    'enabled': True,
    'schedule': '0 0 * * *',  # 每天凌晨执行
    'retention_days': 30,  # 保留30天的备份
    'backup_path': os.path.join(BASE_DIR, 'backups'),
} 