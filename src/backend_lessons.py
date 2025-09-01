import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotel

app = FastAPI()
app.include_router(router_hotel)

if __name__ == "__main__":
    uvicorn.run("backend_lessons:app", host="127.0.0.1", port=8000, reload=True)