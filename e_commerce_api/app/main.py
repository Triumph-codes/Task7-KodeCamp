from contextlib import asynccontextmanager
from fastapi import FastAPI
from colorama import Fore, Style, init

from app.database import create_db_and_tables
from app.routers import products
from app.middleware.timing import TimingMiddleware

init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database and tables on startup."""
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(
    title="E-Commerce API",
    description="A simple e-commerce API with products and a shopping cart.",
    version="0.1.0",
    lifespan=lifespan
)

# Add custom middleware
app.add_middleware(TimingMiddleware)

# Include routers
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API"}