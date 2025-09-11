from fastapi import APIRouter,HTTPException

from src.api.dependecies import DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

from src.api.dependecies import UserIdDeb

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def booking_add(
        booking_data: BookingAddRequest,
        user_id: UserIdDeb,
        db: DBDep,
):
    _room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if _room is None:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    _booking_data = BookingAdd(price=_room.price,user_id=user_id, **booking_data.model_dump())
    booking = await db.bookings.add_(_booking_data)
    await db.commit()
    return {"status":"OK", "data": booking}
