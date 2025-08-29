# app/middleware/ip_logger.py
from fastapi import Request
from colorama import Fore, Style, init

init(autoreset=True)

async def ip_logger_middleware(request: Request, call_next):
    """Logs the client's IP address for every request."""
    client_host = request.client.host
    print(f"{Fore.CYAN}INFO: Request received from IP: {client_host}{Style.RESET_ALL}")
    response = await call_next(request)
    return response