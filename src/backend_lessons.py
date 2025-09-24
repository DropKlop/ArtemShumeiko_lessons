from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend



import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.booking import router as router_booking
from src.api.hotels import router as router_hotel
from src.api.rooms import router as router_room
from src.api.auth import router as router_auth
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.connect()), prefix="fastapi-cache")
    yield
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotel)
app.include_router(router_room)
app.include_router(router_booking)
app.include_router(router_facilities)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("backend_lessons:app", host="127.0.0.1", port=8000, reload=True)