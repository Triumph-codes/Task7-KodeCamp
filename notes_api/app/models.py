from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Add a foreign key to link notes to a user
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # Define a relationship to the User model
    user: Optional["User"] = Relationship(back_populates="notes")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    
    # Define a relationship to the Note model
    notes: List["Note"] = Relationship(back_populates="user")


# --- Pydantic Schemas for Request/Response ---
class NoteCreate(SQLModel):
    title: str
    content: str

class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: Optional[int] = None

class UserCreate(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str