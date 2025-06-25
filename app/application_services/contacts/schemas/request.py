from typing import Optional
from pydantic import BaseModel
from app.models import Contacts

class ContactRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

    @classmethod
    def from_domain(cls, contact: Contacts):
        return cls(
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
        )