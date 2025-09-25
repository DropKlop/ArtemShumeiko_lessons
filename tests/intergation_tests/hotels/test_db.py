from src.database import async_sessionmaker_maker_null_pull
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_create_hotel():
    hotel_data = HotelAdd(title= "Hotel 5 star", location="Краснодар")
    async with DBManager(session_factory=async_sessionmaker_maker_null_pull) as db:
        new_data = await db.hotels.add_(hotel_data)
        await db.commit()
        print(f"{new_data=}")