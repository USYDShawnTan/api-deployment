"""
Vercel Serverless API 入口文件
提供后端 API 服务并处理 Vercel 无服务器环境的兼容性
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from typing import Dict, Any
import secrets
import motor.motor_asyncio
from pydantic import BaseModel

# 环境变量配置
MONGODB_URI = os.environ.get("MONGODB_URI", "")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "api_catalog")
API_ACCESS_PASSWORD = os.environ.get("API_ACCESS_PASSWORD", "")

# 创建 FastAPI 应用
app = FastAPI(
    title="API Service",
    description="RESTful API for web application",
    version="1.0.0"
)

# 安全验证
security = HTTPBasic()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 客户端
client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    """应用启动时连接数据库"""
    global client, db
    if MONGODB_URI:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        db = client[MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    """应用关闭时断开数据库连接"""
    global client
    if client:
        client.close()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """验证 API 访问密码"""
    if not API_ACCESS_PASSWORD:
        return True
    
    correct_password = secrets.compare_digest(credentials.password, API_ACCESS_PASSWORD)
    if not correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True

@app.get("/api")
async def api_root():
    """API 根路径"""
    return {
        "message": "API 服务正常",
        "status": "ok",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    db_status = "connected" if client else "disconnected"
    return {
        "status": "ok",
        "service": "API Service",
        "database": db_status
    }

@app.get("/api/protected", dependencies=[Depends(verify_password)])
async def protected_route():
    """需要密码验证的端点示例"""
    return {"message": "您已成功通过验证", "status": "ok"}

# Vercel Serverless 函数处理 - 直接导出 app
# 不再使用 Mangum，使用标准的 FastAPI 应用
handler = app 