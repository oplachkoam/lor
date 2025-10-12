from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from src.dto.characters import (CharacterResponse, CharactersResponse,
                                CreateCharacterRequest, UpdateCharacterRequest)
from src.dto.errors import CharacterNotFound, NameAlreadyExists
from src.storage.characters import Character, CharactersRepository

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.post("", response_model=CharacterResponse)
async def create_character(request: CreateCharacterRequest):
    character = await CharactersRepository.get_by_name(request.name)
    if character:
        raise NameAlreadyExists()

    character = Character(
        id=uuid4(),
        name=request.name,
        description=request.description,
        created_at=datetime.now()
    )

    await CharactersRepository.create(character)

    return CharacterResponse(
        id=character.id,
        name=character.name,
        description=character.description,
        created_at=character.created_at
    )


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: UUID):
    character = await CharactersRepository.get_by_id(character_id)
    if not character:
        raise CharacterNotFound()

    return CharacterResponse(
        id=character.id,
        name=character.name,
        description=character.description,
        created_at=character.created_at
    )


@router.get("", response_model=CharactersResponse)
async def get_characters():
    characters = await CharactersRepository.list()

    return CharactersResponse(
        characters=[
            CharacterResponse(
                id=character.id,
                name=character.name,
                description=character.description,
                created_at=character.created_at
            ) for character in characters
        ]
    )


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(character_id: UUID,
                           request: UpdateCharacterRequest):
    character = await CharactersRepository.get_by_id(character_id)
    if not character:
        raise CharacterNotFound()

    character.name = request.name
    character.description = request.description
    await CharactersRepository.update(character)

    return CharacterResponse(
        id=character.id,
        name=character.name,
        description=character.description,
        created_at=character.created_at
    )


@router.delete("/{character_id}", response_model=BaseModel)
async def delete_character(character_id: UUID):
    character = await CharactersRepository.get_by_id(character_id)
    if not character:
        raise CharacterNotFound()

    await CharactersRepository.delete(character.id)

    return {}
