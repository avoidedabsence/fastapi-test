from fastapi import FastAPI
import uvicorn
import asyncio

from config import Config
from database.dao import Database
from api.api import router

async def entrypoint():
    await Database.init(Config.DB_URL, Config.DB_MAXCON)

    app = FastAPI(docs_url="/documentation")
    
    app.include_router(router)
    
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