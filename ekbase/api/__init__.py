from fastapi import APIRouter
from .v1 import v1_router

# 创建主路由
api_router = APIRouter(prefix="/api")

# 注册所有版本的路由
api_router.include_router(v1_router)

# 未来可以在这里添加v2版本
# from .v2 import v2_router
# api_router.include_router(v2_router) 