from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select

from app.database import get_session
from app.models import JobApplication, JobApplicationCreate, User
from app.security import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplication, status_code=status.HTTP_201_CREATED)
def create_application(
    application_data: JobApplicationCreate,
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

@router.get("/", response_model=List[JobApplication])
def get_applications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Lists all job applications for the authenticated user."""
    applications = session.exec(
        select(JobApplication).where(JobApplication.user_id == current_user.id)
    ).all()
    return applications

@router.get("/search", response_model=List[JobApplication])
def search_applications(
    status: Optional[str] = Query(None, description="Filter by application status (e.g., 'pending', 'interviewing', 'rejected')"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Searches and filters job applications by status for the authenticated user."""
    query = select(JobApplication).where(JobApplication.user_id == current_user.id)
    
    if status:
        query = query.where(JobApplication.status == status)
    
    applications = session.exec(query).all()
    
    if not applications and status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No applications found with status '{status}'")
    
    return applications