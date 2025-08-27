import json
import os
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()
USERS_FILE = "users.json"

def hash_password(password:  str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_users_db() -> Dict[str, Dict[str, Any]]:
    """Loads user credentials from a JSON file, handling various error cases."""
    # If file doesn't exist, create it with empty dict
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}
    
    try:
        # Check if file is empty
        if os.stat(USERS_FILE).st_size == 0:
            return {}
        
        # Try to read and parse the file
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            
            # Ensure we have a dictionary
            if not isinstance(data, dict):
                raise json.JSONDecodeError("Expected dictionary", "", 0)
                
            return data
            
    except (json.JSONDecodeError, TypeError, ValueError):
        # If file is corrupted, reset it
        print("Warning: users.json file was corrupted. Resetting to empty.")
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

def save_users_db(users_db: Dict[str, Dict[str, Any]]):
    """Saves user credentials to the JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def get_authenticated_user(credentials: HTTPBasicCredentials = Depends(security)) -> Dict[str, Any]:
    """Authenticates a user and returns their user data."""
    users_db = get_users_db()
    user = users_db.get(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return user

def get_current_admin(user: Dict[str, Any] = Depends(get_authenticated_user)) -> Dict[str, Any]:
    """Dependency to check if the authenticated user is an admin."""
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return user

def create_initial_admin_user():
    """Creates a default admin user if one does not exist."""
    users_db = get_users_db()
    if "admin" not in users_db:
        users_db["admin"] = {
            "hashed_password": hash_password("admin_password"),
            "role": "admin"
        }
        with open(USERS_FILE, "w") as f:
            json.dump(users_db, f, indent=4)
        print("Default admin user 'admin' created with password 'admin_password'.")