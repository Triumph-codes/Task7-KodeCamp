from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Dict, Any
import json

from app.database import get_session
from app.models import Student, StudentCreate, StudentUpdate, User, UserLogin
from app.security import get_current_admin, get_authenticated_user, hash_password

router = APIRouter(prefix="/students", tags=["students"])

def get_student_or_404(session: Session, student_id: int) -> Student:
    """Helper function to fetch a student and deserialize their grades."""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")
    
    # We deserialize the grades string here for endpoints that need it
    if student.grades:
        student.grades = json.loads(student.grades)
    else:
        student.grades = {}
    return student

# New helper function for fetching without deserialization
def get_student_for_deletion(session: Session, student_id: int) -> Student:
    """Helper function to fetch a student without deserializing grades."""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found.")
    return student

# --- New Endpoints for Students ---
@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register a new student account (Admin only)")
def register_student_account(
    user_in: UserLogin,
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin)
):
    existing_user = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered."
        )

    hashed_password = hash_password(user_in.password)
    new_user = User(username=user_in.username, hashed_password=hashed_password, role="student")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "Student account registered successfully.", "username": new_user.username}

@router.get("/me", response_model=Student, summary="View my grades (Students only)")
def get_my_grades(
    current_user: User = Depends(get_authenticated_user),
    session: Session = Depends(get_session)
):
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be a student to view this."
        )

    if not current_user.student_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not linked to this user account."
        )
    
    student = get_student_or_404(session, current_user.student_id)
    return student

# --- Admin-only Endpoints ---
@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED, summary="Create a new student record (Admin only)")
def create_student(
    student_in: StudentCreate, 
    session: Session = Depends(get_session), 
    admin_user: User = Depends(get_current_admin)
):
    existing_student = session.exec(select(Student).where(Student.email == student_in.email)).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists."
        )

    user_to_link = session.exec(select(User).where(User.username == student_in.name)).first()
    if not user_to_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User account '{student_in.name}' not found. Create the user account first."
        )

    if user_to_link.student_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User '{user_to_link.username}' is already linked to a student record."
        )
    
    student_data = student_in.model_dump()
    if student_in.grades:
        student_data['grades'] = json.dumps(student_in.grades)
    
    new_student = Student(**student_data)
    
    session.add(new_student)
    session.commit()
    session.refresh(new_student)

    user_to_link.student_id = new_student.id
    session.add(user_to_link)
    session.commit()
    session.refresh(new_student)
    
    new_student.grades = json.loads(new_student.grades)
    return new_student

@router.get("/", response_model=List[Student], summary="Retrieve all students (Admin only)")
def get_all_students(*, session: Session = Depends(get_session), admin_user: User = Depends(get_current_admin)):
    students = session.exec(select(Student)).all()
    for student in students:
        if student.grades:
            student.grades = json.loads(student.grades)
        else:
            student.grades = {}
    return students

@router.get("/{student_id}", response_model=Student, summary="Retrieve a single student by ID (Admin only)")
def get_student_by_id(*, session: Session = Depends(get_session), student_id: int, admin_user: User = Depends(get_current_admin)):
    student = get_student_or_404(session, student_id)
    return student

@router.put("/{student_id}", response_model=Student, summary="Update an existing student (Admin only)")
def update_student(*, session: Session = Depends(get_session), student_id: int, student_in: StudentUpdate, admin_user: User = Depends(get_current_admin)):
    student = get_student_or_404(session, student_id)
    student_data = student_in.model_dump(exclude_unset=True)
    
    if "grades" in student_data:
        student_data['grades'] = json.dumps(student_data['grades'])
    
    for key, value in student_data.items():
        setattr(student, key, value)
    
    session.add(student)
    session.commit()
    session.refresh(student)
    student.grades = json.loads(student.grades)
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student (Admin only)")
def delete_student(*, session: Session = Depends(get_session), student_id: int, admin_user: User = Depends(get_current_admin)):
    # Use the new helper function to get the student without deserializing grades
    student = get_student_for_deletion(session, student_id)
    
    user_to_delete = session.exec(select(User).where(User.student_id == student_id)).first()
    if user_to_delete:
        session.delete(user_to_delete)
        
    session.delete(student)
    session.commit()
    return None