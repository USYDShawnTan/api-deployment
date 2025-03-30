from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import importlib
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("正在初始化应用...")

# 添加当前目录到搜索路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # 创建FastAPI应用
    app = FastAPI(title="API", docs_url="/api/docs", openapi_url="/api/openapi.json")
    logger.info("FastAPI 应用已创建")

    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS 中间件已添加")

    # 导入所有路由模块
    # 假设后端项目使用app/routers目录存放路由
    routers_dir = os.path.join(os.path.dirname(__file__), "app", "routers")
    logger.info(f"加载路由模块目录: {routers_dir}")

    if os.path.exists(routers_dir) and os.path.isdir(routers_dir):
        for filename in os.listdir(routers_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # 去掉.py后缀
                try:
                    module = importlib.import_module(f"app.routers.{module_name}")
                    # 假设每个路由模块都有一个router对象
                    if hasattr(module, "router"):
                        app.include_router(module.router)
                        logger.info(f"已加载路由模块: {module_name}")
                    else:
                        logger.warning(f"模块 {module_name} 中没有找到router对象")
                except Exception as e:
                    logger.error(f"无法导入模块 app.routers.{module_name}: {str(e)}")
    else:
        logger.warning(f"路由目录不存在: {routers_dir}")

    # 添加基本健康检查路由
    @app.get("/")
    async def root():
        return {"message": "API服务正常运行"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

except Exception as e:
    logger.error(f"应用初始化过程中出错: {str(e)}")
    # 如果初始化失败，创建一个基本应用
    app = FastAPI(title="API Fallback")
    
    @app.get("/")
    async def fallback_root():
        return {"message": "API服务正在恢复中，请稍后再试"}
    
    @app.get("/health")
    async def fallback_health():
        return {"status": "recovering", "error": str(e)}

# Vercel处理程序入口点
def handler(request: Request):
    return app(request) 