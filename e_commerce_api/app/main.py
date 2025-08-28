from contextlib import asynccontextmanager
from fastapi import FastAPI
from colorama import Fore, Style, init
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables, get_session
from app.routers import products, users, cart
from app.middleware.timing import TimingMiddleware
from app.security import create_initial_admin_user

init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    with next(get_session()) as session:
        print(f"{Fore.MAGENTA}INFO: Ensuring initial admin user exists...{Style.RESET_ALL}")
        create_initial_admin_user(session)
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(
    title="E-Commerce API",
    description="A simple e-commerce API with products and a shopping cart.",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "null"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Timing Middleware
app.add_middleware(TimingMiddleware)

# Include both routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API"}