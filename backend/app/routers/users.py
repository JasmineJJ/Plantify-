from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    # Check if user already exists
    existing_user = await UserService.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    created_user = await UserService.create_user(user)
    return UserResponse.model_validate(created_user)

@router.get("/", response_model=List[UserResponse])
async def get_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all users with pagination"""
    users = await UserService.get_all_users(skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """Update user by ID"""
    # Check if email is being updated and already exists
    if user_update.email:
        existing_user = await UserService.get_user_by_email(user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="User with this email already exists")
    
    updated_user = await UserService.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(updated_user)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete user by ID"""
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str):
    """Get user by email"""
    user = await UserService.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)