from src.api.dependecies import DBDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

from src.api.dependecies import UserIdDeb

router = APIRouter(prefix="/rooms", tags=["Бронирование"])


@router.post("/{rooms_id}/booking")
async def booking_add(
        booking_data: BookingAddRequest,
        user_id: UserIdDeb,
        db: DBDep,
        rooms_id: int
):
    _price = await db.rooms.get_one_or_none(id=rooms_id)
    _booking_data = BookingAdd(room_id=rooms_id,price=_price,user_id=user_id, **booking_data.model_dump())
    booking = await db.booking.add_(_booking_data)
    await db.commit()
    return {"status":"OK", "data": booking}
