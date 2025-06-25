from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models import Contacts

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, contact: Contacts):
        return cls(
            id=contact.id,
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
            created_at=contact.created_at,
            updated_at=contact.updated_at
        )