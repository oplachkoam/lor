import uvicorn

from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.postgres import Postgres


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
app.include_router(router)


@app.get("/ping", include_in_schema=False)
async def ping():
    return {}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
