from fastapi import Request
from typing import Callable

request_counter = 0

async def request_counter_middleware(request: Request, call_next: Callable):
    """
    A simple middleware that counts and logs the total number of requests.
    """
    global request_counter
    request_counter += 1
    print(f"INFO: Total requests received: {request_counter}")
    
    response = await call_next(request)
    return response

def get_request_count():
    return request_counter