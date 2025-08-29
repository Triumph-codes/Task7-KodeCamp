from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
import json
import os

from app.database import get_session
from app.models import Note, NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

# File path for the notes backup
NOTES_FILE = "notes_backup.json"

### CRUD Endpoints ###
@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    """Creates a new note."""
    db_note = Note.model_validate(note)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@router.get("/", response_model=List[NoteRead])
def get_all_notes(session: Session = Depends(get_session)):
    """Retrieves all notes."""
    notes = session.exec(select(Note)).all()
    return notes

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session: Session = Depends(get_session)):
    """Retrieves a single note by its ID."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    """Deletes a note by its ID."""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"message": "Note deleted successfully"}

### Backup Endpoint ###
@router.post("/backup", status_code=status.HTTP_200_OK)
def backup_notes(session: Session = Depends(get_session)):
    """
    Saves all notes from the database to a local JSON file.
    """
    notes = session.exec(select(Note)).all()
    # Convert SQLModel objects to dictionaries to make them serializable
    notes_dicts = [note.dict() for note in notes]
    
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_dicts, f, ensure_ascii=False, indent=4)
    
    return {"message": f"Successfully backed up {len(notes)} notes to {NOTES_FILE}"}