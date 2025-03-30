"""
Vercel Serverless入口文件 - 极简版
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 创建极简API应用
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
    """根路径响应"""
    return {"message": "API服务正常运行", "status": "ok"}

@app.get("/api")
async def api_root():
    """API路径响应"""
    return {"message": "API根路径正常", "status": "ok"}

@app.get("/api/health")
async def health():
    """健康检查端点"""
    return {"status": "ok", "service": "api.433200.xyz"}

# 用于Vercel Serverless Functions的处理程序
handler = app 