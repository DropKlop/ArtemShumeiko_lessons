from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repos.mapper.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            limit: int,
            offset: int,
            location: str,
            title: str
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in res.scalars().all()]