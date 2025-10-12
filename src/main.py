from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.database.postgres import Postgres
from src.routes.characters import router as characters_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Postgres.connect()
    yield
    await Postgres.close()


app = FastAPI(lifespan=lifespan, title="LOR API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")
app.include_router(characters_router)
app.include_router(router)


@app.get("/ping", include_in_schema=False)
async def ping():
    return {}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
