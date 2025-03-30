"""
Vercel Serverless Functions入口文件
专为Vercel部署环境设计的FastAPI处理程序
"""
import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# 阻止Python生成__pycache__目录
sys.dont_write_bytecode = True

# 设置日志
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义lifespan事件处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动前执行
    logger.info("Vercel Serverless应用启动")
    yield  # 应用运行期间
    logger.info("Vercel Serverless应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title="API服务",
    description="Vercel Serverless环境专用API",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基本路由
@app.get("/")
async def root():
    """API根路径响应，用于健康检查"""
    return {
        "message": "API服务运行正常",
        "service": "api.433200.xyz",
        "status": "operational",
        "version": "1.0.0",
        "environment": "vercel"
    }

# API根路径
@app.get("/api")
async def api_root():
    """API路径响应"""
    return {
        "message": "API根路径正常",
        "endpoints": [
            "/api/health",
            "/api/api_data",
            "/api/catdog",
            "/api/emoji",
            "/api/hitokoto"
        ]
    }

# 健康检查端点
@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    import platform
    return {
        "status": "ok",
        "environment": os.getenv("NODE_ENV", "production"),
        "deployment": "vercel",
        "python_version": platform.python_version(),
    }

# 创建一个简化版API数据端点
@app.get("/api/api_data")
async def get_api_data(password: str = None):
    """获取API数据列表"""
    # 验证密码
    api_password = os.getenv("API_ACCESS_PASSWORD")
    if not password or password != api_password:
        return JSONResponse(
            status_code=401,
            content={"error": "未提供密码或密码错误"}
        )
    
    # 返回一些静态数据作为示例
    return [
        {
            "id": "1",
            "name": "随机表情",
            "path": "/emoji",
            "description": "获取随机表情符号",
            "example": "/emoji?type=random"
        },
        {
            "id": "2",
            "name": "猫狗图片",
            "path": "/catdog",
            "description": "获取随机猫猫或狗狗图片",
            "example": "/catdog?type=cat"
        },
        {
            "id": "3",
            "name": "一言",
            "path": "/hitokoto",
            "description": "获取一条随机名言",
            "example": "/hitokoto"
        }
    ]

# 错误处理
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": {
                "error": "服务器内部错误",
                "message": str(exc)
            }
        }
    )

# 用于Vercel Serverless Functions的处理程序
handler = app 