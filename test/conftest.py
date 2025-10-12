import os
import asyncpg
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from src.database.postgres import Postgres
from src.main import app

os.environ["POSTGRES_URL"] = "postgresql://test:test@localhost:5433/test"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def drop_postgres():
    conn = await asyncpg.connect(os.environ["POSTGRES_URL"])
    try:
        await conn.execute("DELETE FROM locations")
        await conn.execute("DELETE FROM characters")
        yield
        await conn.execute("DELETE FROM locations")
        await conn.execute("DELETE FROM characters")
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    await Postgres.connect()

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    await Postgres.close()
