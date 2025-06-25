from app.application_services.users.users import (
    create_user, get_user, get_all_users, update_user, delete_user, search_users, 
    authenticate_user, get_current_active_user, get_admin_user
)
from app.application_services.users.schemas.request import UserRequest, UserAuthenticateRequest
from app.application_services.users.schemas.response import UserResponse, TokenResponse
from app.models import DB_session
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer

router = APIRouter()

security = HTTPBearer()

@router.get("/", response_model=List[UserResponse])
async def get_all_users_endpoint(
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(DB_session)
):
    """Get all users - Admin only"""
    try:
        return get_all_users(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/search", response_model=List[UserResponse])
async def search_users_endpoint(
    query: str, 
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(DB_session)
):
    """Search users - Admin only"""
    try:
        return search_users(query, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
 
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(
    user_id: int, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Get user by ID - Authenticated users can view their own profile, admins can view any profile"""
    try:
        # Users can only view their own profile unless they're admin
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return get_user(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: int, 
    user: UserRequest, 
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(DB_session)
):
    """Update user - Users can update their own profile, admins can update any profile"""
    try:
        # Users can only update their own profile unless they're admin
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return update_user(user_id, user, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int, 
    current_user: UserResponse = Depends(get_admin_user),
    db: Session = Depends(DB_session)
):
    """Delete user - Admin only"""
    try:
        delete_user(user_id, db)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/auth", response_model=TokenResponse)
async def authenticate_user_endpoint(
    user: UserAuthenticateRequest, 
    db: Session = Depends(DB_session)
):
    """Authenticate user and return JWT token"""
    try:
        return authenticate_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserRequest, 
    db: Session = Depends(DB_session)
):
    """Register new user - Public endpoint"""
    try:
        return create_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/profile", response_model=UserResponse)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current user's profile"""
    return current_user
