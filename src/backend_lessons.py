import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.booking import router as router_booking
from src.api.hotels import router as router_hotel
from src.api.rooms import router as router_room
from src.api.auth import router as router_auth
from src.api.facilities import router as router_facilities

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotel)
app.include_router(router_room)
app.include_router(router_booking)
app.include_router(router_facilities)

if __name__ == "__main__":
    uvicorn.run("backend_lessons:app", host="127.0.0.1", port=8000, reload=True)