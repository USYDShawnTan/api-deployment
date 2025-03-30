from fastapi import FastAPI, Request
import os
import sys
import logging
import traceback
import importlib
import inspect

# 配置日志，确保捕获所有级别的日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("api-deployment")
logger.setLevel(logging.DEBUG)

# 记录基本系统信息
logger.info("="*50)
logger.info("Vercel Python入口点初始化开始")
logger.info(f"Python版本: {sys.version}")
logger.info(f"当前工作目录: {os.getcwd()}")
logger.info(f"文件路径: {os.path.abspath(__file__)}")
logger.info(f"环境变量: PYTHONPATH={os.environ.get('PYTHONPATH', '未设置')}")

# 记录目录结构
logger.info("目录结构检查:")
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"当前目录: {current_dir}")
    files_in_current = os.listdir(current_dir)
    logger.info(f"当前目录文件: {files_in_current}")
    
    # 检查api目录
    api_dir = os.path.join(current_dir, "api")
    if os.path.exists(api_dir):
        logger.info(f"API目录存在: {api_dir}")
        files_in_api = os.listdir(api_dir)
        logger.info(f"API目录文件: {files_in_api}")
        
        # 检查app目录
        app_dir = os.path.join(api_dir, "app")
        if os.path.exists(app_dir):
            logger.info(f"APP目录存在: {app_dir}")
            files_in_app = os.listdir(app_dir)
            logger.info(f"APP目录文件: {files_in_app}")
            
            # 检查routers目录
            routers_dir = os.path.join(app_dir, "routers")
            if os.path.exists(routers_dir):
                logger.info(f"Routers目录存在: {routers_dir}")
                files_in_routers = os.listdir(routers_dir)
                logger.info(f"Routers目录文件: {files_in_routers}")
    else:
        logger.warning(f"API目录不存在: {api_dir}")
except Exception as e:
    logger.error(f"目录检查出错: {str(e)}")
    logger.error(traceback.format_exc())

# 添加搜索路径
original_path = sys.path.copy()
logger.info(f"原始sys.path: {original_path}")

# 添加多个可能的路径
paths_to_add = [
    os.path.dirname(os.path.abspath(__file__)),  # 当前目录
    os.getcwd(),  # 工作目录
    os.path.join(os.getcwd(), "api"),  # api子目录
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.append(path)
        logger.info(f"添加路径到sys.path: {path}")

logger.info(f"更新后的sys.path: {sys.path}")

# 尝试多种导入方式
logger.info("开始尝试导入FastAPI应用...")

app = None
import_errors = []

# 尝试从app.main导入
try:
    logger.info("尝试: from app.main import app")
    from app.main import app
    logger.info("成功从app.main导入FastAPI应用")
    logger.info(f"导入的app类型: {type(app)}")
except Exception as e:
    err_msg = f"从app.main导入应用时出错: {str(e)}"
    logger.error(err_msg)
    logger.error(traceback.format_exc())
    import_errors.append(err_msg)

# 如果上面失败，尝试直接导入
if app is None:
    try:
        logger.info("尝试导入api.app.main")
        import api.app.main
        if hasattr(api.app.main, 'app'):
            app = api.app.main.app
            logger.info("成功从api.app.main导入FastAPI应用")
    except Exception as e:
        err_msg = f"从api.app.main导入应用时出错: {str(e)}"
        logger.error(err_msg)
        logger.error(traceback.format_exc())
        import_errors.append(err_msg)

# 如果仍然失败，尝试动态导入
if app is None:
    try:
        logger.info("尝试使用importlib动态导入")
        for module_name in ["app.main", "api.app.main", "api.run", "app"]:
            try:
                logger.info(f"尝试导入模块: {module_name}")
                module = importlib.import_module(module_name)
                logger.info(f"成功导入模块: {module_name}")
                
                # 检查模块中的所有对象
                for name, obj in inspect.getmembers(module):
                    logger.info(f"检查对象: {name}, 类型: {type(obj)}")
                    if name == "app" and str(type(obj)).find("fastapi") != -1:
                        app = obj
                        logger.info(f"找到FastAPI应用对象: {name}")
                        break
                
                if app:
                    break
            except Exception as e:
                logger.error(f"导入{module_name}时出错: {str(e)}")
                continue
    except Exception as e:
        err_msg = f"动态导入时出错: {str(e)}"
        logger.error(err_msg)
        logger.error(traceback.format_exc())
        import_errors.append(err_msg)

# 如果所有导入都失败，创建一个基本应用
if app is None:
    logger.warning("所有导入尝试都失败，创建一个基本应用")
    logger.warning(f"导入错误汇总: {import_errors}")
    
    app = FastAPI(title="API Fallback", docs_url="/api/docs", openapi_url="/api/openapi.json")
    
    @app.get("/")
    async def fallback_root():
        errors = "\n".join(import_errors)
        return {
            "message": "API服务正在恢复中，请稍后再试", 
            "status": "error",
            "errors": errors,
            "sys_path": sys.path,
            "current_dir": os.getcwd(),
            "files": {
                "current_dir": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
                "api_dir": os.listdir(os.path.join(os.getcwd(), "api")) if os.path.exists(os.path.join(os.getcwd(), "api")) else []
            }
        }
    
    @app.get("/health")
    async def fallback_health():
        return {"status": "recovering", "errors": import_errors}

    @app.get("/debug")
    async def debug():
        return {
            "sys_path": sys.path,
            "current_dir": os.getcwd(),
            "files": {
                "current_dir": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
                "api_dir": os.listdir(os.path.join(os.getcwd(), "api")) if os.path.exists(os.path.join(os.getcwd(), "api")) else []
            },
            "import_errors": import_errors
        }

logger.info("FastAPI应用初始化完成")
logger.info("="*50)

# Vercel处理程序入口点
def handler(request: Request):
    logger.info(f"接收到请求: {request.url.path}")
    return app(request) 