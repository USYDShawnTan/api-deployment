from fastapi import FastAPI, Request
import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("初始化index.py入口文件...")

# 添加当前目录到搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # 从app.main导入app对象
    from app.main import app
    logger.info("成功从app.main导入FastAPI应用")
except Exception as e:
    logger.error(f"从app.main导入应用时出错: {str(e)}")
    # 如果导入失败，创建一个基本应用
    app = FastAPI(title="API Fallback")
    

    @app.get("/health")
    async def fallback_health():
        return {"status": "recovering", "error": str(e)}

# Vercel处理程序入口点
def handler(request: Request):
    return app(request) 