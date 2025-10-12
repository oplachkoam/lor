from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Query
from pydantic import BaseModel

from src.dto.errors import CharacterNotFound, LocationNotFound
from src.dto.locations import (CreateLocationRequest, LocationResponse,
                               LocationsResponse)
from src.storage.characters import CharactersRepository
from src.storage.locations import Location, LocationsRepository

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("", response_model=LocationResponse)
async def create_location(request: CreateLocationRequest):
    character = await CharactersRepository.get_by_id(request.character_id)
    if not character:
        raise CharacterNotFound()

    location = Location(
        id=uuid4(),
        character_id=request.character_id,
        x=request.x,
        y=request.y,
        created_at=request.created_at
    )

    await LocationsRepository.create(location)

    return LocationResponse(
        id=location.id,
        character_id=location.character_id,
        x=location.x,
        y=location.y,
        created_at=location.created_at
    )


@router.get("/{character_id}", response_model=LocationsResponse)
async def get_locations(
        character_id: UUID,
        start: Optional[datetime] = Query(None, description="Начало периода"),
        end: Optional[datetime] = Query(None, description="Конец периода")
):
    character = await CharactersRepository.get_by_id(character_id)
    if not character:
        raise CharacterNotFound()

    locations = await LocationsRepository.get_by_character_id(character_id)

    filtered_locations = [
        loc for loc in locations
        if (start is None or loc.created_at >= start) and
           (end is None or loc.created_at <= end)
    ]

    return LocationsResponse(
        locations=[
            LocationResponse(
                id=location.id,
                character_id=location.character_id,
                x=location.x,
                y=location.y,
                created_at=location.created_at
            ) for location in filtered_locations
        ]
    )


@router.delete("/{location_id}", response_model=BaseModel)
async def delete_location(location_id: UUID):
    location = await LocationsRepository.get_by_id(location_id)
    if not location:
        raise LocationNotFound()

    await LocationsRepository.delete(location.id)

    return {}
