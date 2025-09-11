from fastapi import APIRouter
from typing import Optional


from src.database import async_sessionmaker_maker
from src.repos.rooms import RoomsRepository
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id:int):
    async with async_sessionmaker_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}",
            description="Получение отеля по его ид")
async def get_room(
        hotel_id: int,
        room_id: int
):
    async with async_sessionmaker_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id = room_id, hotel_id = hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_sessionmaker_maker() as session:
        room = await RoomsRepository(session).add_(_room_data)
        await session.commit()
    return {"status":"OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_room(
        hotel_id: int,
        rooms_id: int
):
    async with async_sessionmaker_maker() as session:
        await RoomsRepository(session).del_(hotel_id=hotel_id,id = rooms_id)
        await session.commit()
    return {"status":"OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
        hotel_id: int,
        room_id:Optional[int],
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_sessionmaker_maker() as session:
        await RoomsRepository(session).edit_(_room_data, id = room_id)
        await session.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: Optional[int],
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_sessionmaker_maker() as session:
        await RoomsRepository(session).edit_(room_data, is_patch=True, id = room_id, hotel_id = hotel_id)
        await session.commit()
    return {"status" : "OK"}