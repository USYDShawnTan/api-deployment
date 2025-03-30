from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径响应，用于API健康检查"""
    return {
        "message": "API服务正常运行",
        "service": "api.433200.xyz",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/api")
async def api_root():
    """API根路径响应"""
    return {
        "message": "API根路径正常",
        "endpoints": [
            "/api/api_data",
            "/api/docs",
            "/api/health"
        ]
    }

# 导入应用主模块
from app.main import app as main_app

# 将主应用的路由添加到此应用
app.mount("/api", main_app) 