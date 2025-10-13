from datetime import date

from fastapi import Query, APIRouter, HTTPException
from typing import Optional

from fastapi_cache.decorator import cache

from src.api.dependecies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundExc, check_date, HotelNotFoundHTTPEx
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: Optional[str] = Query("", description="Локация отеля"),
    title: Optional[str] = Query("", description="Наименование отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    check_date(date_from, date_to)
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        location=location,
        title=title,
    )


@router.get("/{hotel_id}", description="Получение отеля по его ид")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExc:
        raise HotelNotFoundHTTPEx


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd):
    hotel = await db.hotels.add_(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}")
async def del_hotel(db: DBDep, hotel_id: Optional[int]):
    await db.hotels.del_(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: Optional[int], hotel_data: HotelAdd):
    await db.hotels.edit_(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep, hotel_id: Optional[int], hotel_data: HotelPatch):
    await db.hotels.edit_(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
