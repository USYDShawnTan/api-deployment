from api import app

# Vercel需要一个handler函数
def handler(request):
    return app(request) 