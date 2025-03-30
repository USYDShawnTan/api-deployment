from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

# 创建FastAPI应用
app = FastAPI(title="API")
logger.info("FastAPI应用已创建")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加API路由
@app.get("/")
async def root():
    return {"message": "API服务正常运行"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy"}

@app.get("/api")
async def api_root():
    return {"message": "API服务正常运行"}

@app.get("/debug")
async def debug():
    # 返回环境信息
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "files": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
        "status": "ok"
    }

@app.get("/api/debug")
async def api_debug():
    # 返回环境信息
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "files": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
        "status": "ok"
    }

# 如果需要处理更多API，可以在这里添加路由
# 例如：从MongoDB获取数据
@app.get("/api/data")
async def get_data():
    return {
        "data": [
            {"id": 1, "name": "测试项目1"},
            {"id": 2, "name": "测试项目2"}
        ],
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 