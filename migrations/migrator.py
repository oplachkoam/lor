import asyncio
import os
from pathlib import Path

import asyncpg


async def main():
    dsn = os.getenv("POSTGRES_URL")
    migrations_dir = os.getenv("MIGRATIONS_DIR")

    if dsn is None or migrations_dir is None:
        raise RuntimeError("Required environment variables must be set")

    conn = await asyncpg.connect(
        dsn, statement_cache_size=0,
        max_cacheable_statement_size=0)
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations
            (
                id   SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            )""")

        applied = set()
        rows = await conn.fetch("SELECT name FROM migrations")
        for row in rows:
            applied.add(row["name"])

        files = sorted([
            f.name for f in Path(migrations_dir).iterdir()
            if f.suffix == ".sql" and f.is_file()
        ])

        if not files:
            print("Empty migrations directory")
            return

        for file in files:
            if file in applied:
                print(f"Migration {file} have already been applied")
                continue

            print(f"Applying {file} migration")
            filepath = Path(migrations_dir) / file
            sql = filepath.read_text()

            async with conn.transaction():
                try:
                    await conn.execute(sql)
                    await conn.execute(
                        "INSERT INTO migrations (name) VALUES ($1)", file
                    )
                    print(f"Migration {file} applied")
                except Exception as e:
                    raise RuntimeError(f"Failed to apply {file}: {e}")

        print("All migrations applied")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
