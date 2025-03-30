"""
Vercel Serverless入口文件 - 简化版，确保Vercel兼容性
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 获取环境变量
MONGODB_URI = os.environ.get("MONGODB_URI", "")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "api_catalog")
API_ACCESS_PASSWORD = os.environ.get("API_ACCESS_PASSWORD", "")

# 创建API应用
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def api_root():
    """API路径响应"""
    return {"message": "API根路径正常", "status": "ok"}

@app.get("/api/health")
async def health():
    """健康检查端点"""
    return {
        "status": "ok", 
        "service": "api.433200.xyz"
    }

# Vercel Serverless函数格式 - 必须按照这个格式
def handler(request, context):
    """Vercel必须的处理函数"""
    return app(request, context)

# 以下处理对象确保正确导出
handler.app = app 