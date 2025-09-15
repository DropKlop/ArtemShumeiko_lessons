from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset
                      ):
        select_query = select(HotelsOrm)
        if location:
            select_query = select_query.filter(func.lower(HotelsOrm.location).contains(location.lower()))
        if title:
            select_query = select_query.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        select_query = (
            select_query
            .limit(limit)
            .offset(offset)
        )
        res = await self.session.execute(select_query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in res.scalars().all()]


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
        hotels_ids = select(RoomsOrm.hotel_id)
        if location:
            hotels_ids = hotels_ids.filter(func.lower(HotelsOrm.location).contains(location.lower()))
        if title:
            hotels_ids = hotels_ids.filter(func.lower(HotelsOrm.title).contains(title.lower()))
        hotels_ids = (
            hotels_ids
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))