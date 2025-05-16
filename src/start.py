from fastapi import FastAPI
from utils.config import Config
from database.dao import Database
import uvicorn
import asyncio

async def entrypoint():
    await Database.init(Config.DB_URL, Config.DB_MAX_CONNECTIONS)

    app = FastAPI()
    
    app.include_router(...)
    
    uc_config = uvicorn.Config(
        app=app,
        host=Config.HOST,
        port=Config.PORT
    )
    
    server = uvicorn.Server(uc_config)
    
    try:
        await server.serve()
    finally:
        await Database.close()
        await server.shutdown()

asyncio.run(entrypoint())