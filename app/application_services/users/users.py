from app.models import Users, DB_session
from sqlalchemy.orm import Session
from app.application_services.users.schemas.request import UserRequest, UserRole, UserAuthenticateRequest
from app.application_services.users.schemas.response import UserResponse
from app.exceptions.exceptions import NotFoundException, UnauthorizedException
from typing import List
from datetime import datetime, timezone
from app.utils.auth import verify_password, get_password_hash, create_access_token, verify_token
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def create_user(user: UserRequest, db: Session) -> UserResponse:
    existing_user = _get_user(user.username, user.email, db)
    if existing_user:
        raise NotFoundException("User already exists")
    
    user_data = user.model_dump()
    # Convert role enum to string for database storage
    if isinstance(user_data.get('role'), UserRole):
        user_data['role'] = user_data['role'].value
    
    db_user = Users(**user_data)
    db_user.password = get_password_hash(user.password)
    db_user.created_at = datetime.now(timezone.utc)
    db_user.updated_at = datetime.now(timezone.utc)
    db.add(db_user)
    db.commit()
    return UserResponse.from_domain(db_user)

def get_user(user_id: int, db: Session) -> UserResponse:
    db_user = _get_user_by_id(user_id, db)
    return UserResponse.from_domain(db_user)

def get_all_users(db: Session) -> List[UserResponse]:
    users = db.query(Users).filter(Users.is_active == True).all()
    if not users:
        raise NotFoundException("No users found")
    return [UserResponse.from_domain(user) for user in users]

def update_user(user_id: int, user: UserRequest, db: Session) -> UserResponse:
    db_user = _get_user_by_id(user_id, db)
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)
    
    # Convert role enum to string for database storage
    if isinstance(user.role, UserRole):
        db_user.role = user.role.value
    else:
        db_user.role = user.role
    
    db_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    return UserResponse.from_domain(db_user)

def delete_user(user_id: int, db: Session) -> None:
    db_user = _get_user_by_id(user_id, db)
    db.delete(db_user)
    db.commit()
    return None

def search_users(query: str, db: Session) -> List[UserResponse]:
    users = db.query(Users).filter(Users.username.ilike(f"%{query}%"), Users.is_active == True).all()
    if not users:
        raise NotFoundException("No users found")
    return [UserResponse.from_domain(user) for user in users]

def authenticate_user(user: UserAuthenticateRequest, db: Session) -> dict:
    db_user = _get_user_by_email(user.email, db)
    if not db_user:
        raise UnauthorizedException("Incorrect email or password")
    if not verify_password(user.password, db_user.password):
        raise UnauthorizedException("Incorrect email or password")
    if not db_user.is_active:
        raise UnauthorizedException("User is not active")
    
    access_token = create_access_token(data={"sub": str(db_user.id), "email": db_user.email, "role": db_user.role})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_domain(db_user)
    }

def _get_user_by_id(user_id: int, db: Session) -> Users:
    db_user = db.query(Users).filter(Users.id == user_id, Users.is_active == True).first()
    if not db_user:
        raise NotFoundException("User not found")
    return db_user

def _get_user_by_email(email: str, db: Session) -> Users:
    db_user = db.query(Users).filter(Users.email == email).first()
    if not db_user:
        return None
    return db_user

def _get_user(username: str, email: str, db: Session) -> Users:
    db_user = db.query(Users).filter((Users.username == username) | (Users.email == email)).first()
    if not db_user:
        return None
    return db_user

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(DB_session)) -> UserResponse:
    try:
        payload = verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing user ID")
        
        # Convert string user ID back to integer
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: invalid user ID")
        
        user = _get_user_by_id(user_id, db)
        return UserResponse.from_domain(user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token validation error: {str(e)}")  # Debug logging
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

async def get_admin_user(current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user