from fastapi import APIRouter, status
from typing import Dict

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """
    健康检查接口
    返回服务状态信息
    """
    return {
        "status": "healthy",
        "message": "Service is running normally"
    }
