from src.repos.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.repos.mapper.mappers import BookingDataMapper

class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper