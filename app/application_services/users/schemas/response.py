from pydantic import BaseModel
from datetime import datetime
from app.models import Users
from app.utils.auth import UserRole

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: Users):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
class UserAuthenticateResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    @classmethod
    def from_domain(cls, user: Users):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role
        )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse