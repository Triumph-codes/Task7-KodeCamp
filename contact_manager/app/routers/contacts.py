# app/routers/contacts.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Contact, ContactBase, ContactRead, ContactUpdate, User
from app.security import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactBase, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_contact = Contact.model_validate(contact)
    db_contact.user_id = current_user.id
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

@router.get("/", response_model=List[ContactRead])
def get_user_contacts(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    contacts = session.exec(select(Contact).where(Contact.user_id == current_user.id)).all()
    return contacts

@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int, 
    contact_in: ContactUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_contact = session.exec(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found or you don't have permission to update it")
    
    contact_data = contact_in.model_dump(exclude_unset=True)
    db_contact.sqlmodel_update(contact_data)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    contact = session.exec(select(Contact).where(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found or you don't have permission to delete it")
    
    session.delete(contact)
    session.commit()
    return