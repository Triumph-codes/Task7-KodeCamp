# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style, init

from app.database import create_db_and_tables
from app.routers import users, contacts
from app.middleware.ip_logger import ip_logger_middleware

init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(
    title="Contact Manager API",
    description="A secure API for managing personal contacts.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For a live project, use specific origins like your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IP Logger Middleware
app.middleware("http")(ip_logger_middleware)

# Include Routers
app.include_router(users.router)
app.include_router(contacts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Manager API"}