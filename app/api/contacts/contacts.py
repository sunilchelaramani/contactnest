from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.application_services.contacts.schemas.response import ContactResponse
from app.application_services.contacts.schemas.request import ContactRequest
from app.application_services.contacts.contacts import add_contact, get_contacts, get_contact_details, update_contact_details, delete_contact, search_contacts as search_contacts_service
from app.application_services.users.users import get_current_active_user
from app.application_services.users.schemas.response import UserResponse
from app.models import DB_session
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactRequest, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Create a new contact - Authenticated users only"""
    try:
        return add_contact(contact, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/", response_model=List[ContactResponse])
async def list_contacts(
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """List all contacts - Authenticated users only"""
    try:
        return get_contacts(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Get contact details - Authenticated users only"""
    try:
        return get_contact_details(contact_id, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, 
    contact: ContactRequest, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Update contact details - Authenticated users only"""
    try:
        return update_contact_details(contact_id, contact, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(
    contact_id: int, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Delete contact - Authenticated users only"""
    try:
        delete_contact(contact_id, db)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts_endpoint(
    query: str, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Search contacts - Authenticated users only"""
    try:
        return search_contacts_service(query, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))