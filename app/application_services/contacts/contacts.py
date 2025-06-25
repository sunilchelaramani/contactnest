from typing import List
from sqlalchemy.orm import Session
from app.models import Contacts
from app.application_services.contacts.schemas.request import ContactRequest
from app.application_services.contacts.schemas.response import ContactResponse
from app.exceptions.exceptions import NotFoundException
from datetime import datetime, timezone


def add_contact(contact: ContactRequest, db: Session) -> ContactResponse:
    db_contact = Contacts(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    return ContactResponse.from_domain(db_contact)

def get_contacts(db: Session, limit: int = 10, offset: int = 0) -> List[ContactResponse]:
    contacts = db.query(Contacts).limit(limit).offset(offset).all()
    if not contacts:
        raise NotFoundException("No contacts found")
    return [ContactResponse.from_domain(contact) for contact in contacts]

def get_contact_details(contact_id: int, db: Session) -> ContactResponse:
    contact = _get_contact_by_id(contact_id, db)
    return ContactResponse.from_domain(contact)

def update_contact_details(contact_id: int, contact: ContactRequest, db: Session) -> ContactResponse:
    db_contact = _get_contact_by_id(contact_id, db)
    db_contact.name = contact.name
    db_contact.email = contact.email
    db_contact.phone = contact.phone
    db_contact.updated_at = datetime.now(timezone.utc)
    db.commit()
    return ContactResponse.from_domain(db_contact)

def delete_contact(contact_id: int, db: Session) -> None:
    db_contact = _get_contact_by_id(contact_id, db)
    db.delete(db_contact)
    db.commit()

def search_contacts(query: str, db: Session) -> List[ContactResponse]:
    contacts = db.query(Contacts).filter(Contacts.name.ilike(f"%{query}%") | Contacts.email.ilike(f"%{query}%")).all()
    if not contacts:
        raise NotFoundException("No contacts found")
    return [ContactResponse.from_domain(contact) for contact in contacts]

def _get_contact_by_id(contact_id: int, db: Session) -> Contacts:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if not contact:
        raise NotFoundException("No contacts found")
    return contact