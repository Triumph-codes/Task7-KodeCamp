# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from colorama import Fore, Style, init
from sqlmodel import Session, select

from app.database import create_db_and_tables, get_session
from app.routers import users, listings # Changed from 'applications' to 'listings'
from app.middleware.user_agent import UserAgentMiddleware
from app.security import hash_password
from app.models import User

init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes database and tables on startup."""
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    with next(get_session()) as session:
        print(f"{Fore.MAGENTA}INFO: Ensuring initial users exist...{Style.RESET_ALL}")
        # Create a default admin user
        if not session.exec(select(User).where(User.username == "admin")).first():
            hashed_password = hash_password("admin_password")
            admin_user = User(username="admin", hashed_password=hashed_password, role="admin")
            session.add(admin_user)
            session.commit()
            print("Default admin user 'admin' created with password 'admin_password'.")

        # Create a default regular user
        if not session.exec(select(User).where(User.username == "testuser")).first():
            hashed_password = hash_password("test_password")
            regular_user = User(username="testuser", hashed_password=hashed_password, role="user")
            session.add(regular_user)
            session.commit()
            print("Default user 'testuser' created with password 'test_password'.")
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(
    title="Job Application Tracker API",
    description="An API to track job applications for authenticated users.",
    version="0.1.0",
    lifespan=lifespan
)

# Add custom middleware
app.add_middleware(UserAgentMiddleware)

# Include routers
app.include_router(users.router)
app.include_router(listings.router) # Changed from 'applications' to 'listings'

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Application Tracker API"}