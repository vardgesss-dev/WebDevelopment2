from contextlib import asynccontextmanager

from fastapi import FastAPI
from api.router import common_router

from core.handlers import register_exception_handlers
from core.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(common_router)
register_exception_handlers(app)
