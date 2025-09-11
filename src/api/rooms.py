from fastapi import APIRouter
from typing import Optional

from src.api.dependecies import DBDep
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id:int
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}",
            description="Получение отеля по его ид")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    return await db.rooms.get_one_or_none(id = room_id, hotel_id = hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add_(_room_data)
    await db.commit()
    return {"status":"OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_room(
        db: DBDep,
        hotel_id: int,
        rooms_id: int
):
    await db.rooms.del_(hotel_id=hotel_id,id = rooms_id)
    await db.commit()
    return {"status":"OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
        db: DBDep,
        hotel_id: int,
        room_id:Optional[int],
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit_(_room_data, id = room_id)
    await db.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: Optional[int],
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit_(room_data, is_patch=True, id = room_id, hotel_id = hotel_id)
    await db.commit()
    return {"status" : "OK"}