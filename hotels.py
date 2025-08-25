from fastapi import Query, Body, APIRouter
from typing import Optional

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name":"sochi"},
    {"id": 2, "title": "Dubai", "name":"dubai"}
]

@router.get("")
def get_hotels(
        id: Optional[int] = Query(None, description="Айди"),
        title: Optional[str] = Query(None, description="Наименование отеля")
):
    if not id or not title:
        return hotels
    return [hotel for hotel in hotels if hotel["title"] == title or hotel["id"] == id]


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
        title: str = Body(),
        name: str = Body(),
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status" : "OK", "new hotel" : hotel}
        return {"status" : "hotel not found"}
    return {"status" : "not ok"}


@router.patch("/{hotel_id}")
def patch_hotel(
        hotel_id: Optional[int],
        title: Optional[str] = Body(None),
        name: Optional[str] = Body(None)
):
    if hotel_id:
        for hotel in hotels:
            if hotel["id"]==hotel_id:
                if title:
                    hotel["title"] = title
                if name:
                    hotel["name"] = name
                return {"status":"OK", "new hotel":hotel}
        return {"status" : "hotel not found"}
    return {"status":"hotel id not pass"}