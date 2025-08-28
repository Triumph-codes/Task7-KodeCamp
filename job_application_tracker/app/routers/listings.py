from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlmodel import Session, select

from app.database import get_session
from app.models import JobListing, JobListingCreate, JobApplication, JobApplicationCreate, User
from app.security import get_current_user, get_current_admin

router = APIRouter(prefix="/listings", tags=["listings"])

### Public Endpoints ###
@router.get("/", response_model=List[JobListing], description="Retrieves all public job listings. No authentication required.")
def get_all_listings(session: Session = Depends(get_session)):
    """Retrieves all public job listings."""
    listings = session.exec(select(JobListing)).all()
    return listings

@router.get("/search", response_model=List[JobListing], description="Searches for job listings by position or company. No authentication required.")
def search_listings(
    position: Optional[str] = Query(None, description="Search by job position"),
    company: Optional[str] = Query(None, description="Search by company name"),
    session: Session = Depends(get_session)
):
    """Searches for job listings by position or company."""
    query = select(JobListing)

    if position:
        query = query.where(JobListing.position.like(f"%{position}%"))
    if company:
        query = query.where(JobListing.company.like(f"%{company}%"))

    listings = session.exec(query).all()
    return listings

### User-Specific Endpoints ###
@router.post("/apply", response_model=JobApplication, status_code=status.HTTP_201_CREATED, description="Allows an authenticated user to apply to a job listing.")
def apply_to_listing(
    application_data: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Allows an authenticated user to apply to a job listing."""
    listing = session.get(JobListing, application_data.listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Job listing not found.")
    
    # Check if the user has already applied to this listing
    existing_application = session.exec(
        select(JobApplication).where(
            JobApplication.user_id == current_user.id,
            JobApplication.listing_id == application_data.listing_id
        )
    ).first()
    if existing_application:
        raise HTTPException(status_code=409, detail="You have already applied to this listing.")

    new_application = JobApplication(
        user_id=current_user.id,
        listing_id=application_data.listing_id
    )
    session.add(new_application)
    session.commit()
    session.refresh(new_application)
    return new_application

@router.get("/my-applications", response_model=List[JobApplication], description="Retrieves all job applications for the authenticated user.")
def get_my_applications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Retrieves all job applications for the authenticated user."""
    applications = session.exec(
        select(JobApplication).where(JobApplication.user_id == current_user.id)
    ).all()
    return applications

### Admin-Only Endpoints ###
@router.post(
        "/", 
        response_model=JobListing,
        status_code=status.HTTP_201_CREATED,
        summary="Create a new job listing (Admin Only)")
def create_listing(
    listing_data: JobListingCreate,
    current_admin: User = Depends(get_current_admin), # Use the admin dependency
    session: Session = Depends(get_session)
):
    """Allows an admin to create a new job listing."""
    listing = JobListing(
        company=listing_data.company,
        position=listing_data.position,
        description=listing_data.description,
        creator_id=current_admin.id
    )
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing

@router.put(
        "/{listing_id}",
        response_model=JobListing,
        summary="Update a job listing (Admin Only)")
def update_listing(
    listing_id: int,
    listing_data: JobListingCreate,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Allows an admin to update a job listing by ID."""
    listing = session.get(JobListing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    
    listing.company = listing_data.company
    listing.position = listing_data.position
    listing.description = listing_data.description
    
    session.add(listing)
    session.commit()
    session.refresh(listing)
    return listing

@router.delete(
        "/{listing_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete a job listing (Admin Only)")

def delete_listing(
    listing_id: int,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Allows an admin to delete a job listing by ID."""
    listing = session.get(JobListing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    
    session.delete(listing)
    session.commit()
    return

@router.get(
        "/all-applications",
        response_model=List[JobApplication],
        summary="View all job applications (Admin Only)")
def get_all_applications(
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    """Allows an admin to view all job applications from all users."""
    applications = session.exec(select(JobApplication)).all()
    return applications