# app/database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///contacts.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Creates the database and all tables defined in SQLModel."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session