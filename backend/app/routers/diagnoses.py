from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.diagnosis import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse
from app.services.diagnosis_service import DiagnosisService

router = APIRouter(prefix="/diagnoses", tags=["diagnoses"])

@router.post("/", response_model=DiagnosisResponse)
async def create_diagnosis(diagnosis: DiagnosisCreate):
    """Create a new diagnosis"""
    created_diagnosis = await DiagnosisService.create_diagnosis(diagnosis)
    if not created_diagnosis:
        raise HTTPException(status_code=400, detail="Plant not found or invalid data")
    return DiagnosisResponse.model_validate(created_diagnosis)

@router.get("/", response_model=List[DiagnosisResponse])
async def get_diagnoses(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all diagnoses with pagination"""
    diagnoses = await DiagnosisService.get_all_diagnoses(skip=skip, limit=limit)
    return [DiagnosisResponse.model_validate(diagnosis) for diagnosis in diagnoses]

@router.get("/{diagnosis_id}", response_model=DiagnosisResponse)
async def get_diagnosis(diagnosis_id: int):
    """Get diagnosis by ID"""
    diagnosis = await DiagnosisService.get_diagnosis_by_id(diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return DiagnosisResponse.model_validate(diagnosis)

@router.put("/{diagnosis_id}", response_model=DiagnosisResponse)
async def update_diagnosis(diagnosis_id: int, diagnosis_update: DiagnosisUpdate):
    """Update diagnosis by ID"""
    updated_diagnosis = await DiagnosisService.update_diagnosis(diagnosis_id, diagnosis_update)
    if not updated_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return DiagnosisResponse.model_validate(updated_diagnosis)

@router.delete("/{diagnosis_id}")
async def delete_diagnosis(diagnosis_id: int):
    """Delete diagnosis by ID"""
    success = await DiagnosisService.delete_diagnosis(diagnosis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    return {"message": "Diagnosis deleted successfully"}

@router.get("/plant/{plant_id}", response_model=List[DiagnosisResponse])
async def get_diagnoses_by_plant(plant_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all diagnoses for a specific plant"""
    diagnoses = await DiagnosisService.get_diagnoses_by_plant(plant_id, skip=skip, limit=limit)
    return [DiagnosisResponse.model_validate(diagnosis) for diagnosis in diagnoses]

@router.get("/user/{user_id}", response_model=List[DiagnosisResponse])
async def get_diagnoses_by_user(user_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """Get all diagnoses for a specific user"""
    diagnoses = await DiagnosisService.get_diagnoses_by_user(user_id, skip=skip, limit=limit)
    return [DiagnosisResponse.model_validate(diagnosis) for diagnosis in diagnoses]