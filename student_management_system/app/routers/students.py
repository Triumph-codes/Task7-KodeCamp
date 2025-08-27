from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Dict, Any
import json # Import the json library

from app.database import get_session
from app.models import Student, StudentCreate, StudentUpdate
from app.security import get_current_admin

router = APIRouter(
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_current_admin)],
)

def get_student_or_404(session: Session, student_id: int) -> Student:
    """Helper function to fetch a student or raise a 404 error."""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found."
        )
    # Deserialize the grades string back into a dictionary
    if student.grades:
        student.grades = json.loads(student.grades)
    else:
        student.grades = {}
    return student

# --- CRUD Endpoints ---

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED, summary="Create a new student")
def create_student(*, session: Session = Depends(get_session), student_in: StudentCreate):
    """
    Creates a new student entry in the database.
    **Note**: This operation requires admin privileges.
    """
    existing_student = session.exec(select(Student).where(Student.email == student_in.email)).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student with this email already exists."
        )
    
    # Serialize the grades dictionary to a JSON string
    student_data = student_in.model_dump()
    if student_in.grades:
        student_data['grades'] = json.dumps(student_in.grades)
    
    new_student = Student(**student_data)
    session.add(new_student)
    session.commit()
    session.refresh(new_student)
    
    # Return a response with grades as a dictionary
    new_student.grades = json.loads(new_student.grades)
    return new_student

@router.get("/", response_model=List[Student], summary="Retrieve all students")
def get_all_students(*, session: Session = Depends(get_session)):
    """
    Retrieves a list of all student entries from the database.
    **Note**: This operation requires admin privileges.
    """
    students = session.exec(select(Student)).all()
    # Deserialize the grades string for each student
    for student in students:
        if student.grades:
            student.grades = json.loads(student.grades)
        else:
            student.grades = {}
    return students

@router.get("/{student_id}", response_model=Student, summary="Retrieve a single student by ID")
def get_student_by_id(*, session: Session = Depends(get_session), student_id: int):
    """
    Retrieves a single student's details by their unique ID.
    **Note**: This operation requires admin privileges.
    """
    student = get_student_or_404(session, student_id)
    return student

@router.put("/{student_id}", response_model=Student, summary="Update an existing student")
def update_student(*, session: Session = Depends(get_session), student_id: int, student_in: StudentUpdate):
    """
    Updates an existing student's details based on their ID.
    **Note**: This operation requires admin privileges.
    """
    student = get_student_or_404(session, student_id)
    student_data = student_in.model_dump(exclude_unset=True)
    
    if "grades" in student_data:
        student_data['grades'] = json.dumps(student_data['grades'])
    
    # Update the student object with the new data
    for key, value in student_data.items():
        setattr(student, key, value)
    
    session.add(student)
    session.commit()
    session.refresh(student)
    
    # Return a response with grades as a dictionary
    student.grades = json.loads(student.grades)
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student")
def delete_student(*, session: Session = Depends(get_session), student_id: int):
    """
    Deletes a student entry from the database by their ID.
    **Note**: This operation requires admin privileges.
    """
    student = get_student_or_404(session, student_id)
    session.delete(student)
    session.commit()
    return None