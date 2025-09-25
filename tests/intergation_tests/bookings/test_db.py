from datetime import date

from src.schemas.bookings import BookingAdd, Booking


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from= date(year=2025, month=8, day=10),
        date_to= date(year=2025, month=8, day=20),
        price= 100
    )
    new_booking_data = await db.bookings.add_(booking_data)
    # Получить бронь
    new_booking_data = await db.bookings.get_one_or_none(id = new_booking_data.id)
    assert new_booking_data is not None
    # Обновить бронь
    new_booking_data.price = 250
    await db.bookings.edit_(new_booking_data)
    # Удалить бронь
    await db.bookings.del_(id = new_booking_data.id)

    await db.commit()