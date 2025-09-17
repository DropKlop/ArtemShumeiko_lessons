from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self,
                                   hotel_id,
                                   date_from: date,
                                   date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        select_query = (
                        select(self.model)
                        .options(selectinload(self.model.facilities))
                        .filter(RoomsOrm.id.in_(rooms_ids_to_get))
                        )
        res = await self.session.execute(select_query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in res.scalars().all()]


    async def get_one_or_none_with_facility(self, **filter_by):
        select_query = (
            select(self.model)
            .filter_by(**filter_by)
            .options(selectinload(self.model.facilities))
                        )
        res = await self.session.execute(select_query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model, from_attributes=True)
