import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from colorama import Fore, Style, init

init(autoreset=True)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        print(f"{Fore.CYAN}Request: {request.method} {request.url.path} | Process Time: {process_time:.4f}s{Style.RESET_ALL}")
        return response