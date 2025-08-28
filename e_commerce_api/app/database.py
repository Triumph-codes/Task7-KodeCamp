from sqlmodel import create_engine, Session, SQLModel

# Define the database file name
sqlite_file_name = "e_commerce.db"
# Create the SQLAlchemy engine for SQLite
sqlite_url = f"sqlite:///{sqlite_file_name}"

# `connect_args` is a SQLAlchemy-specific argument for SQLite to handle multi-threading
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Creates all database tables defined in the models."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get a database session."""
    with Session(engine) as session:
        yield session