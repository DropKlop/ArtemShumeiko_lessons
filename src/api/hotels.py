from fastapi import Query, APIRouter, Body
from typing import Optional


from src.api.dependecies import PaginationDep
from src.database import async_sessionmaker_maker
from src.repos.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: Optional[str] = Query("", description="Локация отеля"),
        title: Optional[str] = Query("", description="Наименование отеля")
):
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)
    async with async_sessionmaker_maker() as session:
        return await HotelsRepository(session).get_all(location = location, title = title, limit =limit or 5, offset = offset)


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_sessionmaker_maker() as session:
        hotel = await HotelsRepository(session).add_(hotel_data)
        await session.commit()
    return {"status":"OK", "data": hotel}




@router.delete("/{hotel_id}")
def del_hotel(
        hotel_id: Optional[int]
):
    if hotel_id:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                hotels.remove(hotel)
                return hotels
        return {"status":"Не найден отель"}
    return {"status":"не указан айди"}


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id:Optional[int],
        hotel_data: Hotel
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"status" : "OK", "new hotel" : hotel}
        return {"status" : "hotel not found"}
    return {"status" : "not ok"}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: Optional[int],
        hotel_data: HotelPatch
):
    if hotel_id:
        for hotel in hotels:
            if hotel["id"]==hotel_id:
                if hotel_data.title:
                    hotel["title"] = hotel_data.title
                if hotel_data.name:
                    hotel["name"] = hotel_data.name
                return {"status":"OK", "new hotel":hotel}
        return {"status" : "hotel not found"}
    return {"status":"hotel id not pass"}