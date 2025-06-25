from pydantic import BaseModel
from app.models import Users
from typing import Optional
from app.utils.auth import UserRole

class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[UserRole] = UserRole.USER

    @classmethod
    def from_domain(cls, user: Users):
        return cls(
            username=user.username,
            email=user.email,
            password=user.password,
            role=user.role
        )
    
class UserAuthenticateRequest(BaseModel):
    email: str
    password: str

    @classmethod
    def from_domain(cls, user: Users):
        return cls(
            email=user.email,
            password=user.password
        )