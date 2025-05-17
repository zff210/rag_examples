from fastapi import FastAPI
from contextlib import asynccontextmanager
from ekbase.api import api_router 
from ekbase.database.init_db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动前执行
    init()
    init_database()  # 初始化数据库
    load_documents()
    yield
    # 关闭时执行
    save_documents()
    # 可以在这里添加清理代码

# 创建FastAPI应用
app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(api_router)

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)