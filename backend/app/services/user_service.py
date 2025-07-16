from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from tortoise.exceptions import DoesNotExist

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        """Create a new user"""
        return await User.create(**user_data.model_dump())
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return await User.get(email=email)
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_all_users(skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return await User.all().offset(skip).limit(limit)
    
    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user by ID"""
        try:
            user = await User.get(id=user_id)
            update_data = user_data.model_dump(exclude_unset=True)
            if update_data:
                await user.update_from_dict(update_data)
                await user.save()
            return user
        except DoesNotExist:
            return None
    
    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete user by ID"""
        try:
            user = await User.get(id=user_id)
            await user.delete()
            return True
        except DoesNotExist:
            return False
    
    @staticmethod
    async def get_users_count() -> int:
        """Get total count of users"""
        return await User.all().count()