from typing import List, Optional
from app.models.plant import Plant
from app.models.user import User
from app.schemas.plant import PlantCreate, PlantUpdate
from tortoise.exceptions import DoesNotExist

class PlantService:
    @staticmethod
    async def create_plant(plant_data: PlantCreate) -> Optional[Plant]:
        """Create a new plant"""
        try:
            # Verify user exists
            user = await User.get(id=plant_data.user_id)
            plant_dict = plant_data.model_dump()
            plant_dict['user_id'] = plant_dict.pop('user_id')
            return await Plant.create(user=user, **{k: v for k, v in plant_dict.items() if k != 'user_id'})
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_plant_by_id(plant_id: int) -> Optional[Plant]:
        """Get plant by ID with user relationship"""
        try:
            return await Plant.get(id=plant_id).prefetch_related('user')
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_all_plants(skip: int = 0, limit: int = 100) -> List[Plant]:
        """Get all plants with pagination"""
        return await Plant.all().prefetch_related('user').offset(skip).limit(limit)
    
    @staticmethod
    async def get_plants_by_user(user_id: int, skip: int = 0, limit: int = 100) -> List[Plant]:
        """Get all plants for a specific user"""
        return await Plant.filter(user_id=user_id).prefetch_related('user').offset(skip).limit(limit)
    
    @staticmethod
    async def update_plant(plant_id: int, plant_data: PlantUpdate) -> Optional[Plant]:
        """Update plant by ID"""
        try:
            plant = await Plant.get(id=plant_id)
            update_data = plant_data.model_dump(exclude_unset=True)
            if update_data:
                await plant.update_from_dict(update_data)
                await plant.save()
            return await Plant.get(id=plant_id).prefetch_related('user')
        except DoesNotExist:
            return None
    
    @staticmethod
    async def delete_plant(plant_id: int) -> bool:
        """Delete plant by ID"""
        try:
            plant = await Plant.get(id=plant_id)
            await plant.delete()
            return True
        except DoesNotExist:
            return False
    
    @staticmethod
    async def get_plants_count() -> int:
        """Get total count of plants"""
        return await Plant.all().count()
    
    @staticmethod
    async def get_plants_count_by_user(user_id: int) -> int:
        """Get count of plants for a specific user"""
        return await Plant.filter(user_id=user_id).count()