from typing import Optional, List
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

# User and JobApplication models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str

    applications: List["JobApplication"] = Relationship(back_populates="user")

class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    status: str = Field(default="pending")
    date_applied: date = Field(default_factory=date.today)
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    user: Optional[User] = Relationship(back_populates="applications")

# Pydantic schemas for request/response validation
class UserCreate(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class JobApplicationCreate(SQLModel):
    """Schema for creating a new job application."""
    company: str
    position: str
    status: Optional[str] = "pending"