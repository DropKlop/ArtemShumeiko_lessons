from datetime import date

from sqlalchemy import select

from src.repos.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.repos.mapper.mappers import BookingDataMapper

class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_booking_with_today_check_in(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]