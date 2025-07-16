from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.plant import PlantCreate, PlantUpdate, PlantResponse
from app.services.plant_service import PlantService

router = APIRouter(prefix="/plants", tags=["plants"])

@router.post("/", response_model=PlantResponse)
async def create_plant(plant: PlantCreate):
    """Create a new plant"""
    created_plant = await PlantService.create_plant(plant)
    if not created_plant:
        raise HTTPException(status_code=400, detail="User not found or invalid data")
    return PlantResponse.model_validate(created_plant)

@router.get("/", response_model=List[PlantResponse])
async def get_plants(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all plants with pagination"""
    plants = await PlantService.get_all_plants(skip=skip, limit=limit)
    return [PlantResponse.model_validate(plant) for plant in plants]

@router.get("/{plant_id}", response_model=PlantResponse)
async def get_plant(plant_id: int):
    """Get plant by ID"""
    plant = await PlantService.get_plant_by_id(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return PlantResponse.model_validate(plant)

@router.put("/{plant_id}", response_model=PlantResponse)
async def update_plant(plant_id: int, plant_update: PlantUpdate):
    """Update plant by ID"""
    updated_plant = await PlantService.update_plant(plant_id, plant_update)
    if not updated_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return PlantResponse.model_validate(updated_plant)

@router.delete("/{plant_id}")
async def delete_plant(plant_id: int):
    """Delete plant by ID"""
    success = await PlantService.delete_plant(plant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"message": "Plant deleted successfully"}

@router.get("/user/{user_id}", response_model=List[PlantResponse])
async def get_plants_by_user(user_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all plants for a specific user"""
    plants = await PlantService.get_plants_by_user(user_id, skip=skip, limit=limit)
    return [PlantResponse.model_validate(plant) for plant in plants]