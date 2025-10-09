from fastapi import APIRouter, HTTPException

from src.api.dependecies import DBDep
from src.exceptions import ObjectNotFoundExc, RoomCannotBeBookedExc
from src.schemas.bookings import BookingAdd, BookingAddRequest

from src.api.dependecies import UserIdDeb

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def booking_add(
    booking_data: BookingAddRequest,
    user_id: UserIdDeb,
    db: DBDep,
):
    try:
        _room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundExc:
        raise HTTPException(status_code=404, detail="Номер не найден")
    _hotel = await db.hotels.get_one(id=_room.hotel_id)
    _booking_data = BookingAdd(
        price=_room.price, user_id=user_id, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=_hotel.id)
    except RoomCannotBeBookedExc as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_all_booking(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_my_booking(db: DBDep, user_id: UserIdDeb):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}
