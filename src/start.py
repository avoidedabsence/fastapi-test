from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import uvicorn
import asyncio

from config import Config
from database.dao import Database
from api import router
from test_data import create_test_data

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await Database.init(Config.DB_URL, Config.DB_MAXCON)
    await create_test_data()
    
    yield
    
    await Database.close()

app = FastAPI(
    lifespan=lifespan,
    title="nebus testing task",
    description=(
        "t.me/avoidedabsence"
    )
)

app.include_router(router)

@app.get("/")
async def root():
    return RedirectResponse("/docs")