from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlantBase(BaseModel):
    name: str
    species: str
    description: Optional[str] = None

class PlantCreate(PlantBase):
    user_id: int

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    description: Optional[str] = None

class PlantResponse(PlantBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True