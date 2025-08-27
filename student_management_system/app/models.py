from typing import Optional, Dict, Any, List
from sqlmodel import Field, SQLModel, Relationship, JSON, String
import json


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = "student" # Default role is student

    # One-to-one relationship with Student model
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", unique=True)
    student: Optional["Student"] = Relationship(back_populates="user")

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int
    email: str = Field(unique=True)
    grades: str = Field(default="{}")

    # One-to-one relationship with User model
    user: Optional[User] = Relationship(back_populates="student")

class StudentCreate(SQLModel):
    name: str
    age: int
    email: str
    grades: Dict[str, Any] = {}

class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    grades: Optional[Dict[str, Any]] = None

class UserLogin(SQLModel):
    username: str
    password: str