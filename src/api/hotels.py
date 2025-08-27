from fastapi import Query, APIRouter, Body
from typing import Optional

from src.api.dependecies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name":"sochi"},
    {"id": 2, "title": "Dubai", "name":"dubai"},
    {"id": 3, "title": "Saint-Peterburg", "name":"spb"}
]

@router.get("")
def get_hotels(
        id: Optional[int] = Query(None, description="Айди"),
        title: Optional[str] = Query(None, description="Наименование отеля")
):
    if not id or not title:
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]

@router.get("/pagination")
def hotel_pagination(
        pagination: PaginationDep
):
    page = pagination.per_page * (pagination.page - 1)
    return hotels[page:pagination.per_page]



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
def create_hotel(hotel_data: Hotel = Body(openapi_examples={"1":{"summary":"Сочи", "value":{
        "title": "Сочи у моря",
        "name":"Сочи"
    }}})):
    new_hotel = {
            "id":hotels[-1]["id"] + 1,
            "title":hotel_data.title,
            "name":hotel_data.name
    }
    hotels.append(new_hotel)
    return {"status":"OK", "new_hotel":new_hotel}

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