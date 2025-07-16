from typing import List, Optional
from app.models.diagnosis import Diagnosis
from app.models.plant import Plant
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate
from tortoise.exceptions import DoesNotExist

class DiagnosisService:
    @staticmethod
    async def create_diagnosis(diagnosis_data: DiagnosisCreate) -> Optional[Diagnosis]:
        """Create a new diagnosis"""
        try:
            # Verify plant exists
            plant = await Plant.get(id=diagnosis_data.plant_id)
            diagnosis_dict = diagnosis_data.model_dump()
            diagnosis_dict['plant_id'] = diagnosis_dict.pop('plant_id')
            return await Diagnosis.create(plant=plant, **{k: v for k, v in diagnosis_dict.items() if k != 'plant_id'})
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_diagnosis_by_id(diagnosis_id: int) -> Optional[Diagnosis]:
        """Get diagnosis by ID with plant and user relationships"""
        try:
            return await Diagnosis.get(id=diagnosis_id).prefetch_related('plant', 'plant__user')
        except DoesNotExist:
            return None
    
    @staticmethod
    async def get_all_diagnoses(skip: int = 0, limit: int = 100) -> List[Diagnosis]:
        """Get all diagnoses with pagination"""
        return await Diagnosis.all().prefetch_related('plant', 'plant__user').offset(skip).limit(limit)
    
    @staticmethod
    async def get_diagnoses_by_plant(plant_id: int, skip: int = 0, limit: int = 100) -> List[Diagnosis]:
        """Get all diagnoses for a specific plant"""
        return await Diagnosis.filter(plant_id=plant_id).prefetch_related('plant', 'plant__user').offset(skip).limit(limit)
    
    @staticmethod
    async def get_diagnoses_by_user(user_id: int, skip: int = 0, limit: int = 100) -> List[Diagnosis]:
        """Get all diagnoses for a specific user (through their plants)"""
        return await Diagnosis.filter(plant__user_id=user_id).prefetch_related('plant', 'plant__user').offset(skip).limit(limit)
    
    @staticmethod
    async def update_diagnosis(diagnosis_id: int, diagnosis_data: DiagnosisUpdate) -> Optional[Diagnosis]:
        """Update diagnosis by ID"""
        try:
            diagnosis = await Diagnosis.get(id=diagnosis_id)
            update_data = diagnosis_data.model_dump(exclude_unset=True)
            if update_data:
                await diagnosis.update_from_dict(update_data)
                await diagnosis.save()
            return await Diagnosis.get(id=diagnosis_id).prefetch_related('plant', 'plant__user')
        except DoesNotExist:
            return None
    
    @staticmethod
    async def delete_diagnosis(diagnosis_id: int) -> bool:
        """Delete diagnosis by ID"""
        try:
            diagnosis = await Diagnosis.get(id=diagnosis_id)
            await diagnosis.delete()
            return True
        except DoesNotExist:
            return False
    
    @staticmethod
    async def get_diagnoses_count() -> int:
        """Get total count of diagnoses"""
        return await Diagnosis.all().count()
    
    @staticmethod
    async def get_diagnoses_count_by_plant(plant_id: int) -> int:
        """Get count of diagnoses for a specific plant"""
        return await Diagnosis.filter(plant_id=plant_id).count()
    
    @staticmethod
    async def get_diagnoses_count_by_user(user_id: int) -> int:
        """Get count of diagnoses for a specific user"""
        return await Diagnosis.filter(plant__user_id=user_id).count()