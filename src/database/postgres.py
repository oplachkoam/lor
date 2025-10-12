import logging
import os
from typing import Optional

import asyncpg
from asyncpg import Pool

logger = logging.getLogger(__name__)


class Postgres:
    _pool: Optional[Pool] = None

    @staticmethod
    async def connect() -> None:
        database_url = os.getenv("POSTGRES_URL")
        if not database_url:
            raise ValueError("POSTGRES_URL environment "
                             "variable is not set")

        try:
            # noinspection PyUnresolvedReferences
            Postgres._pool = await asyncpg.create_pool(
                database_url, min_size=1, max_size=10)
            logger.info("Postgres connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create postgres pool: {e}")
            raise

    @staticmethod
    async def pool():
        return Postgres._pool

    @staticmethod
    async def close():
        await Postgres._pool.close()
        logger.info("Postgres connection pool closed")
