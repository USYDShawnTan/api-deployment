"""
Vercel Serverless入口文件 - 支持MongoDB连接
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB连接
MONGODB_URI = os.environ.get("MONGODB_URI", "")
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "api_catalog")
API_ACCESS_PASSWORD = os.environ.get("API_ACCESS_PASSWORD", "")

# 创建API应用
app = FastAPI()

# MongoDB客户端
client = None
db = None

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    """启动时连接MongoDB"""
    global client, db
    try:
        if MONGODB_URI:
            client = AsyncIOMotorClient(MONGODB_URI)
            db = client[MONGODB_DB_NAME]
            print(f"Connected to MongoDB: {MONGODB_DB_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """关闭时断开MongoDB连接"""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")

@app.get("/")
async def root():
    """根路径响应"""
    return {"message": "API服务正常运行", "status": "ok"}

@app.get("/api")
async def api_root():
    """API路径响应"""
    return {"message": "API根路径正常", "status": "ok"}

@app.get("/api/health")
async def health():
    """健康检查端点"""
    db_status = "connected" if client else "disconnected"
    return {
        "status": "ok", 
        "service": "api.433200.xyz",
        "database": db_status
    }

@app.get("/api/api_data")
async def get_api_data(password: str = ""):
    """获取API数据"""
    # 验证密码
    if password != API_ACCESS_PASSWORD:
        return JSONResponse(
            status_code=401,
            content={"error": "未授权访问", "message": "密码错误"}
        )
    
    try:
        # 从数据库获取数据
        if db:
            collection = db["apis"]
            api_list = await collection.find({}).to_list(length=100)
            # 处理MongoDB的ObjectId
            for api in api_list:
                api["_id"] = str(api["_id"])
            return api_list
        else:
            # 如果没有数据库连接，返回模拟数据
            return [
                {
                    "id": "1",
                    "name": "随机表情",
                    "path": "/emoji",
                    "description": "获取随机表情符号",
                    "example": "/emoji?type=random",
                    "params": [{"name": "type", "description": "表情类型", "required": False}]
                },
                {
                    "id": "2",
                    "name": "猫狗图片",
                    "path": "/catdog",
                    "description": "获取随机猫猫或狗狗图片",
                    "example": "/catdog?type=cat",
                    "params": [{"name": "type", "description": "动物类型 (cat/dog)", "required": True}]
                }
            ]
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "服务器错误", "message": str(e)}
        )

# 用于Vercel Serverless Functions的处理程序
handler = app 