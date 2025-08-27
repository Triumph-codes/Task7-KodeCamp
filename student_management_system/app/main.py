import time
import json
import os
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from colorama import Fore, Style, init 

from app.database import create_db_and_tables, get_session
from app.routers import students
from app.security import create_initial_admin_user
from sqlmodel import Session

init(autoreset=True)
LOG_FILE = "request_log.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"{Fore.MAGENTA}INFO: Creating database and tables...{Style.RESET_ALL}")
    create_db_and_tables()
    with next(get_session()) as session:
        print(f"{Fore.MAGENTA}INFO: Ensuring initial admin user exists...{Style.RESET_ALL}")
        create_initial_admin_user(session)
    yield
    print(f"{Fore.MAGENTA}INFO: Application shutdown complete.{Style.RESET_ALL}")

app = FastAPI(lifespan=lifespan)

# --- Middleware ---
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "path": request.url.path,
        "method": request.method,
        "client_host": request.client.host,
        "response_status": response.status_code,
        "process_time_ms": round(process_time * 1000, 2)
    }

    try:
        if not os.path.exists(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
            with open(LOG_FILE, "w") as f:
                json.dump([log_entry], f, indent=4)
        else:
            with open(LOG_FILE, "r+") as f:
                data = json.load(f)
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=4)
    except Exception as e:
        print(f"{Fore.RED}ERROR: Failed to write to log file: {e}{Style.RESET_ALL}")
        
    return response

# --- Routers ---
app.include_router(students.router)

# --- Root Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Management API"}