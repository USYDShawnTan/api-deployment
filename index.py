"""
Vercel部署入口文件
此文件作为Vercel Python运行时的入口点
用于将请求转发到FastAPI应用
"""
import sys
import os

# 阻止Python生成__pycache__目录
sys.dont_write_bytecode = True

# 导入应用的处理程序
from app.main import app as fastapi_app

# 为Vercel Serverless Functions导出处理函数
handler = fastapi_app

# 直接运行测试
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000) 