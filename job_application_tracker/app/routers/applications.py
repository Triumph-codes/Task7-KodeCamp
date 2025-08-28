from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select

from app.database import get_session
from app.models import JobApplication, JobApplicationCreate, User
from app.security import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplication, status_code=status.HTTP_201_CREATED)
def create_application(
    application_data: JobApplicationCreate, # Use the new schema here
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Adds a new job application for the authenticated user."""
    # Create the full JobApplication model instance with the user_id
    application = JobApplication(
        company=application_data.company,
        position=application_data.position,
        status=application_data.status,
        user_id=current_user.id
    )

    session.add(application)
    session.commit()
    session.refresh(application)
    return application