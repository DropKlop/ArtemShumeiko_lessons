from fastapi import Query, APIRouter, Body
from typing import Optional

from sqlalchemy import insert, select, or_

from src.api.dependecies import PaginationDep
from src.database import async_sessionmaker_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: Optional[str] = Query(None, description="Локация отеля"),
        title: Optional[str] = Query(None, description="Наименование отеля")
):
    limit = pagination.per_page
    offset = pagination.per_page * (pagination.page - 1)
    async with async_sessionmaker_maker() as session:
        select_query = (
            select(HotelsOrm)
            .filter(
                or_(
                    HotelsOrm.location.like(f"%{location}%"),
                    HotelsOrm.title.like(f"%{title}%")
                )
            )
            .limit(limit)
            .offset(offset)
        )

        res = await session.execute(select_query)
        hotels = res.scalars().all()
        return hotels

    #if pagination.page and pagination.per_page
      #  return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]



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

@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={"1":{"summary":"Сочи", "value":{
        "title": "Сочи у моря",
        "location":"Сочи"
    }}})):

    async with async_sessionmaker_maker() as session:
        add_hotel_statement = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_statement)
        await session.commit()

    return {"status":"OK"}

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