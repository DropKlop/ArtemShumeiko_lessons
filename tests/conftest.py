import json

import pytest

from src.backend_lessons import app
from src.config import settings
from src.database import Base, engine_null_pull
from src.models import *

from httpx import ASGITransport, AsyncClient

@pytest.fixture(scope="session", autouse=True)
def check_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



@pytest.fixture(scope="session", autouse=True)
async def test_root(setup_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test") as ac:
         await ac.post("/auth/register",
                                 json={
                                     "email":"pupis@pes.com",
                                     "password": "pupis123"
                                 })