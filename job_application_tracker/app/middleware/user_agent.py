from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

class UserAgentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "user-agent" not in request.headers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User-Agent header is missing."
            )
        return await call_next(request)