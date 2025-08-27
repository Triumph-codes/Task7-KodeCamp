import json
import os
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict, Any
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_authenticated_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Authenticates a user and returns their user data from the database."""
    user = session.exec(select(User).where(User.username == credentials.username)).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return user

def get_current_admin(user: User = Depends(get_authenticated_user)) -> User:
    """Dependency to check if the authenticated user is an admin."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )
    return user

def create_initial_admin_user(session: Session) -> None:
    """Creates a default admin user if one does not exist in the database."""
    admin_user = session.exec(select(User).where(User.username == "admin")).first()
    if not admin_user:
        hashed_password = hash_password("admin_password")
        new_admin = User(username="admin", hashed_password=hashed_password, role="admin")
        session.add(new_admin)
        session.commit()
        print("Default admin user 'admin' created with password 'admin_password'.")