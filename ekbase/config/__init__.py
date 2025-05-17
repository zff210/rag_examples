import os
from .settings import *

# 根据环境变量加载对应的配置
env = os.getenv('EK_ENV', 'development')
if env == 'development':
    from .development import *
elif env == 'production':
    from .production import *
else:
    raise ValueError(f"Unknown environment: {env}")

# 确保必要的目录存在
for path in [
    os.path.join(BASE_DIR, 'data'),
    os.path.join(BASE_DIR, 'logs'),
    STORAGE['documents'],
    STORAGE['vectors'],
    STORAGE['temp'],
]:
    os.makedirs(path, exist_ok=True) 