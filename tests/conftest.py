import json

import pytest

from src.backend_lessons import app
from src.config import settings
from src.database import Base, engine_null_pull, async_sessionmaker_maker_null_pull
from src.models import *

from httpx import ASGITransport, AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    #после создания добавим сразу тестовые данные
    hotels = json_to_model("tests/mock_hotels.json", HotelAdd)
    rooms = json_to_model("tests/mock_rooms.json", RoomAdd)

    async with DBManager(session_factory=async_sessionmaker_maker_null_pull) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

def json_to_model(file_src:str, model):
    with open(file_src, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [model.model_validate(item) for item in data]



@pytest.fixture(scope="session", autouse=True)
async def test_root(setup_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test") as ac:
         await ac.post("/auth/register",
                                 json={
                                     "email":"pupis@pes.com",
                                     "password": "pupis123"
                                 })