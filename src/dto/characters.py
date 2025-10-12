from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateCharacterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64,
                      description="Имя персонажа")
    description: Optional[str] = Field(None, description="Описание персонажа")


class CharacterResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime


class CharactersResponse(BaseModel):
    characters: List[CharacterResponse]


class UpdateCharacterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64,
                      description="Имя персонажа")
    description: Optional[str] = Field(None, description="Описание персонажа")
