from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NoteCreate(SQLModel):
    title: str
    content: str

class NoteRead(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime