from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style, init
import os

from app.database import create_db_and_tables, get_session
from app.routers import notes, users


# Initialize colorama
init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes database and tables on startup.
    """
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(
    title="Notes API",
    description="An API to manage personal notes with a database and file backup.",
    version="0.1.0",
    lifespan=lifespan
)

# Define allowed origins for CORS


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the custom request counter middleware
@app.middleware("http")
async def request_counter_middleware(request: Request, call_next):
    from app.middleware.request_counter import request_counter, get_request_count
    request_counter += 1
    print(f"INFO: Total requests received: {request_counter}")
    response = await call_next(request)
    return response

# Include routers
app.include_router(notes.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Notes API"}