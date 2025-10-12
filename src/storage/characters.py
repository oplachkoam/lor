from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.database.postgres import Postgres


class Character(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime


class Users:
    @staticmethod
    async def create(character: Character) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("INSERT INTO characters (id, name, description, "
                     "created_at) VALUES ($1, $2, $3)")
            await conn.execute(
                query, character.id, character.name,
                character.description, character.created_at)

    @staticmethod
    async def get_by_id(id: UUID) -> Optional[Character]:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("SELECT id, name, description, created_at "
                     "FROM characters WHERE id = $1")
            row = await conn.fetchrow(query, id)
            return Character(**row) if row else None

    @staticmethod
    async def list() -> List[Character]:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("SELECT id, name, description, created_at "
                     "FROM characters ORDER BY name")
            rows = await conn.fetch(query)
            return [Character(**row) for row in rows]

    @staticmethod
    async def update(character: Character) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("UPDATE characters SET name = $1, description = $2, "
                     "created_at = $3 WHERE id = $4")
            await conn.execute(
                query, character.name, character.description,
                character.created_at, character.id)

    @staticmethod
    async def delete(id: UUID) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = "DELETE FROM characters WHERE id = $1"
            await conn.execute(query, id)
