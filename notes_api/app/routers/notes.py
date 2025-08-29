# app/routers/notes.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
import json
import os

from app.database import get_session
from app.models import Note, NoteCreate, NoteRead, User # Import the User model
from app.security import get_current_user # Import the security dependency

router = APIRouter(prefix="/notes", tags=["notes"])

# File path for the notes backup
NOTES_FILE = "notes_backup.json"

### CRUD Endpoints ###
@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user), # Add this dependency
    session: Session = Depends(get_session)
):
    """Creates a new note for the authenticated user."""
    db_note = Note.model_validate(note)
    db_note.user_id = current_user.id # Link the note to the user
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteRead])
def get_all_notes(
    current_user: User = Depends(get_current_user), # Add this dependency
    session: Session = Depends(get_session)
):
    """Retrieves all notes for the authenticated user."""
    # Retrieve notes belonging only to the current user
    notes = session.exec(select(Note).where(Note.user_id == current_user.id)).all()
    return notes

@router.get("/{note_id}", response_model=NoteRead)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user), # Add this dependency
    session: Session = Depends(get_session)
):
    """Retrieves a single note by its ID for the authenticated user."""
    note = session.exec(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user), # Add this dependency
    session: Session = Depends(get_session)
):
    """Deletes a note by its ID for the authenticated user."""
    note = session.exec(
        select(Note).where(Note.id == note_id, Note.user_id == current_user.id)
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return

# The backup endpoint is not protected .
@router.post("/backup", status_code=status.HTTP_200_OK)
def backup_notes(session: Session = Depends(get_session)):
    """
    Saves all notes from the database to a local JSON file.
    """
    notes = session.exec(select(Note)).all()
    # Create a new list of dictionaries, converting 'datetime' objects to strings
    notes_dicts = []
    for note in notes:
        note_dict = note.model_dump()
        note_dict['created_at'] = note_dict['created_at'].isoformat()
        notes_dicts.append(note_dict)

    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_dicts, f, ensure_ascii=False, indent=4)
    return {"message": f"Successfully backed up {len(notes)} notes to {NOTES_FILE}"}