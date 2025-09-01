from sqlalchemy import select, insert


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        select_query = select(self.model)
        res = await self.session.execute(select_query)
        return res.scalars().all()

    async def get_one_or_none(self, **filter_by):
        select_query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(select_query)

        return res.scalars().one_or_none()

    async def add_(self,data_):
        add_hotel_statement = insert(self.model).values(**data_.model_dump())
        await self.session.execute(add_hotel_statement)
        return data_