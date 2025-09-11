from fastapi import Query, APIRouter
from typing import Optional


from src.api.dependecies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: Optional[str] = Query("", description="Локация отеля"),
        title: Optional[str] = Query("", description="Наименование отеля")
):
    limit = pagination.per_page or 5
    offset = limit * (pagination.page - 1)
    return await db.hotels.get_all(location = location, title = title, limit =limit or 5, offset = offset)


@router.get("/{hotel_id}",
            description="Получение отеля по его ид")
async def get_hotel(
        db: DBDep,
        hotel_id: int
):
    return await db.hotels.get_one_or_none(id = hotel_id)


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd
):
    hotel = await db.hotels.add_(hotel_data)
    await db.commit()
    return {"status":"OK", "data": hotel}


@router.delete("/{hotel_id}")
async def del_hotel(
        db: DBDep,
        hotel_id: Optional[int]
):
    await db.hotels.del_(id = hotel_id)
    await db.commit()
    return {"status":"OK"}


@router.put("/{hotel_id}")
async def put_hotel(
        db: DBDep,
        hotel_id:Optional[int],
        hotel_data: HotelAdd
):
    await db.hotels.edit_(hotel_data, id = hotel_id)
    await db.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(
        db: DBDep,
        hotel_id: Optional[int],
        hotel_data: HotelPatch
):
    await db.hotels.edit_(hotel_data, is_patch=True, id = hotel_id)
    await db.commit()
    return {"status" : "OK"}