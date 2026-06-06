# health_check.py - وب سرور جداگانه برای Health Check
from aiohttp import web
import asyncio
import threading

async def health_check(request):
    return web.Response(text="OK")

async def start_health_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("✅ Health check server started on port 10000")

def run_health_server():
    asyncio.run(start_health_server())

# وقتی این فایل مستقیم اجرا بشه
if __name__ == "__main__":
    run_health_server()
