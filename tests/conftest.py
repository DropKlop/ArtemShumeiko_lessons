import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependecies import get_db
from src.backend_lessons import app
from src.config import settings
from src.database import Base, engine_null_pull, async_sessionmaker_maker_null_pull
from src.models import *

from httpx import ASGITransport, AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


async def get_db_null_pool():
    async with DBManager(session_factory=async_sessionmaker_maker_null_pull) as db:
        yield db

@pytest.fixture()
async def db():
    async for db in get_db_null_pool():
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
def check_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    hotels = json_to_model("tests/mock_hotels.json", HotelAdd)
    rooms = json_to_model("tests/mock_rooms.json", RoomAdd)

    async with DBManager(session_factory=async_sessionmaker_maker_null_pull) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

def json_to_model(file_src:str, model):
    with open(file_src, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [model.model_validate(item) for item in data]

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def test_root(ac, setup_db):
    await ac.post("/auth/register",
        json={
            "email":"pupis@pes.com",
            "password": "pupis123"
        })


@pytest.fixture(scope="session")
async def authenticated_ac(test_root, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "pupis@pes.com",
            "password": "pupis123"
        })
    assert "access_token" in ac.cookies
    yield ac