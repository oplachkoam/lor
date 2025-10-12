from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from src.database.postgres import Postgres


class Location(BaseModel):
    id: UUID
    character_id: UUID
    x: float
    y: float
    created_at: datetime


class Locations:
    @staticmethod
    async def create(location: Location) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("INSERT INTO locations (id, character_id, x, y, "
                     "created_at) VALUES ($1, $2, $3, $4, $5)")
            await conn.execute(
                query, location.id, location.character_id,
                location.x, location.y, location.created_at)

    @staticmethod
    async def get_by_id(id: UUID) -> Optional[Location]:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("SELECT id, character_id, x, y, created_at "
                     "FROM locations WHERE id = $1")
            row = await conn.fetchrow(query, id)
            return Location(**row) if row else None

    @staticmethod
    async def get_by_character_id(character_id: UUID) -> List[Location]:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("SELECT id, character_id, x, y, created_at "
                     "FROM locations WHERE character_id = $1 "
                     "ORDER BY created_at")
            rows = await conn.fetch(query, character_id)
            return [Location(**row) for row in rows]

    @staticmethod
    async def list() -> List[Location]:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("SELECT id, character_id, x, y, created_at "
                     "FROM locations ORDER BY created_at")
            rows = await conn.fetch(query)
            return [Location(**row) for row in rows]

    @staticmethod
    async def update(location: Location) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = ("UPDATE locations SET character_id = $1, "
                     "x = $2, y = $3, created_at = $4 WHERE id = $5")
            await conn.execute(
                query, location.character_id, location.x,
                location.y, location.created_at, location.id)

    @staticmethod
    async def delete(id: UUID) -> None:
        pool = await Postgres.pool()

        async with pool.acquire() as conn:
            query = "DELETE FROM locations WHERE id = $1"
            await conn.execute(query, id)
