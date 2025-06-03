from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
import logging.config
import os
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 设置环境变量，禁用多进程
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from ekbase.api import api_router 
from ekbase.database.init_db import init_database
from ekbase.core.services.document_core_service import DocumentCoreService
from ekbase.config import SERVER, LOGGING, CORS, LLM


def init():
    # 确保日志目录存在
    os.makedirs(LOGGING['log_dir'], exist_ok=True)
    
    # 配置日志
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("初始化日志成功")
        logger.info(f"日志文件存储位置: {LOGGING['log_dir']}")
        logger.debug(f"环境变量文件路径: {env_path}")
        logger.debug(f"环境变量文件是否存在: {env_path.exists()}")
        logger.debug(f'api_key:{LLM['api_key']}')
        
        # 初始化数据库
        init_database()
        logger.info("初始化数据库成功")
        
        # 初始化文档服务
        document_service = DocumentCoreService()
        document_service.load_documents()
        logger.info("初始化文档服务成功")
        
    except Exception as e:
        logger.error(f"初始化失败: {str(e)}", exc_info=True)
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的初始化
    init()
    yield
    # 关闭时的清理工作
    logger = logging.getLogger(__name__)
    logger.info("应用程序正在关闭...")
    
    # 清理资源
    try:
        # 清理多进程资源
        import multiprocessing
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
        
        # 清理其他资源
        if hasattr(app.state, 'llm_utils'):
            app.state.llm_utils._cleanup()
        
        logger.info("资源清理完成")
    except Exception as e:
        logger.error(f"资源清理过程中发生错误: {str(e)}", exc_info=True)

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS['origins'],
    allow_methods=CORS['methods'],
    allow_headers=CORS['headers'],
)

# 注册路由
app.include_router(api_router)

# 启动应用
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"SERVER: {SERVER}")
        uvicorn.run(
            "ekbase.main:app",
            host=SERVER['host'],
            port=SERVER['port'],
            reload=SERVER['reload'],
            reload_dirs=SERVER['reload_dirs']
        )
        
        logger.info("服务启动成功")
        logger.info(f"服务运行于: http://{SERVER['host']}:{SERVER['port']}")
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}", exc_info=True)
        raise