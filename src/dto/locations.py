from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class CreateLocationRequest(BaseModel):
    character_id: UUID = Field(..., description="ID персонажа")
    x: float = Field(..., description="Координата X")
    y: float = Field(..., description="Координата Y")
    created_at: datetime = Field(..., description="Время создания локации")


class LocationResponse(BaseModel):
    id: UUID
    character_id: UUID
    x: float
    y: float
    created_at: datetime


class LocationsResponse(BaseModel):
    locations: List[LocationResponse]
