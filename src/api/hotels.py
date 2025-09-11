from fastapi import Query, APIRouter
from typing import Optional


from src.api.dependecies import PaginationDep
from src.database import async_sessionmaker_maker
from src.repos.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, HotelAdd

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


@router.get("/{hotel_id}",
            description="Получение отеля по его ид")
async def get_hotel(
        hotel_id: int
):
    async with async_sessionmaker_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id = hotel_id)


@router.post("")
async def create_hotel(hotel_data: HotelAdd):
    async with async_sessionmaker_maker() as session:
        hotel = await HotelsRepository(session).add_(hotel_data)
        await session.commit()
    return {"status":"OK", "data": hotel}


@router.delete("/{hotel_id}")
async def del_hotel(
        hotel_id: Optional[int]
):
    async with async_sessionmaker_maker() as session:
        await HotelsRepository(session).del_(id = hotel_id)
        await session.commit()
    return {"status":"OK"}


@router.put("/{hotel_id}")
async def put_hotel(
        hotel_id:Optional[int],
        hotel_data: HotelAdd
):
    async with async_sessionmaker_maker() as session:
        await HotelsRepository(session).edit_(hotel_data, id = hotel_id)
        await session.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(
        hotel_id: Optional[int],
        hotel_data: HotelPatch
):
    async with async_sessionmaker_maker() as session:
        await HotelsRepository(session).edit_(hotel_data, is_patch=True, id = hotel_id)
        await session.commit()
    return {"status" : "OK"}