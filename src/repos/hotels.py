from sqlalchemy import select, func

from src.repos.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

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

        return res.scalars().all()
