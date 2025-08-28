from typing import Optional, List
from datetime import date
from sqlmodel import Field, SQLModel, Relationship

# User model with a role
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = "user"  # Default role is "user"

    applications: List["JobApplication"] = Relationship(back_populates="user")
    listings: List["JobListing"] = Relationship(back_populates="creator")

# New model for admin-created job listings
class JobListing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    description: Optional[str] = None
    
    # Link to the user who created the listing (the admin)
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional[User] = Relationship(back_populates="listings")
    
    # Relationship to applications for this listing
    applications: List["JobApplication"] = Relationship(back_populates="listing")

# Model for a user's specific application
class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: str = Field(default="pending")
    date_applied: date = Field(default_factory=date.today)
    
    # Link to the user who applied
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="applications")

    # Link to the job listing being applied to
    listing_id: Optional[int] = Field(default=None, foreign_key="joblisting.id")
    listing: Optional["JobListing"] = Relationship(back_populates="applications")

# Pydantic schemas for request/response validation
class UserCreate(SQLModel):
    username: str
    password: str
    role: Optional[str] = "user"

class Token(SQLModel):
    access_token: str
    token_type: str

class JobListingCreate(SQLModel):
    company: str
    position: str
    description: Optional[str] = None

class JobApplicationCreate(SQLModel):
    listing_id: int