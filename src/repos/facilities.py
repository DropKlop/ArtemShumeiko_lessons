from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repos.base import BaseRepository
from src.repos.mapper.mappers import FacilityDataMapper
from sqlalchemy import select, delete, insert


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = FacilityDataMapper

    async def set_rooms_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        current_facilities_ids: list[int] = res.scalars().all()
        ids_to_delete: list[int] = list(
            set(current_facilities_ids) - set(facilities_ids)
        )
        ids_to_insert: list[int] = list(
            set(facilities_ids) - set(current_facilities_ids)
        )

        if ids_to_delete:
            delete_m2m_facilities_stms = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )

            await self.session.execute(delete_m2m_facilities_stms)

        if ids_to_insert:
            insert_m2m_facilities_stms = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )

            await self.session.execute(insert_m2m_facilities_stms)
