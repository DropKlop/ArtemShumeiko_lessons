from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel


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

    async def add_(self,data_: BaseModel):
        add_data_statement = insert(self.model).values(**data_.model_dump()).returning(self.model)
        res = await self.session.execute(add_data_statement)
        return res.scalars().one()

    async def del_(self,**filter_by) -> None:
        delete_obj = delete(self.model).where(self.model.id == filter_by["id_"])
        await self.session.execute(delete_obj)

    async def edit_(self, data: BaseModel, **filter_by) -> None:
        edit_obj = update(self.model).where(self.model.id == filter_by["id"]).values(**data.model_dump())
        await self.session.execute(edit_obj)