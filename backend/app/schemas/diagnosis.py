from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiagnosisBase(BaseModel):
    disease_name: str
    confidence_score: float
    image_path: str
    notes: Optional[str] = None
    is_healthy: bool = False

class DiagnosisCreate(DiagnosisBase):
    plant_id: int

class DiagnosisUpdate(BaseModel):
    disease_name: Optional[str] = None
    confidence_score: Optional[float] = None
    image_path: Optional[str] = None
    notes: Optional[str] = None
    is_healthy: Optional[bool] = None

class DiagnosisResponse(DiagnosisBase):
    id: int
    plant_id: int
    created_at: datetime

    class Config:
        from_attributes = True