from src.repos.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking