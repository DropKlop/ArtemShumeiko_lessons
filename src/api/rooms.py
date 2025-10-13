from datetime import date

from fastapi import APIRouter, HTTPException
from typing import Optional

from fastapi.params import Query

from src.api.dependecies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    if date_from > date_to:
        raise HTTPException(status_code=409, detail="Дата заезда позже даты выезда")
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}", description="Получение отеля по его ид")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none_with_facility(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add_(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_room(db: DBDep, hotel_id: int, rooms_id: int):
    await db.rooms.del_(hotel_id=hotel_id, id=rooms_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
    db: DBDep, hotel_id: int, room_id: Optional[int], room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit_(_room_data, id=room_id)
    await db.rooms_facilities.set_rooms_facilities(
        room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
    db: DBDep, hotel_id: int, room_id: Optional[int], room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit_(room_data, is_patch=True, id=room_id, hotel_id=hotel_id)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_rooms_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()
    return {"status": "OK"}
