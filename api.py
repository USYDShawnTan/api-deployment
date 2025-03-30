from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")
logger.info("启动API服务")

# 创建应用 - 简化配置
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础路由 - 尽量简单
@app.get("/")
def root():
    return {"message": "API服务正常运行"}

@app.get("/api")
def api_root():
    return {"message": "API服务正常运行"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/health")
def api_health():
    return {"status": "healthy"}

@app.get("/api/data")
def get_data():
    try:
        return {
            "data": [
                {"id": 1, "name": "示例数据1"},
                {"id": 2, "name": "示例数据2"}
            ],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"获取数据时出错: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/debug")
def debug():
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "files": os.listdir(os.getcwd()),
        "status": "ok"
    } 