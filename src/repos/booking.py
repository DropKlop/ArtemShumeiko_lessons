from datetime import date

from sqlalchemy import select

from src.repos.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.repos.mapper.mappers import BookingDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_check_in(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )

        res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book = res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add_(data)
            return new_booking
        else:
            return Exception
