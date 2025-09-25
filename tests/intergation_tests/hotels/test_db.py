from src.schemas.hotels import HotelAdd


async def test_create_hotel(db):
    hotel_data = HotelAdd(title= "Hotel 5 star", location="Краснодар")
    await db.hotels.add_(hotel_data)
    await db.commit()