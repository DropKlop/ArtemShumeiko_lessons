import logging
import sqlalchemy.exc
from asyncpg import UniqueViolationError
from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from src.exceptions import ObjectNotFoundExc, ObjectAlreadyExsistExc
from src.repos.mapper.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        select_query = select(self.model).filter(*filter).filter_by(**filter_by)
        res = await self.session.execute(select_query)
        return [
            self.mapper.map_to_domain_entity(model) for model in res.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        select_query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(select_query)
        model = res.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        select_query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(select_query)
        try:
            model = res.scalars_one()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectNotFoundExc
        return self.mapper.map_to_domain_entity(model)

    async def add_(self, data_: BaseModel):
        try:
            add_data_statement = (
                insert(self.model).values(**data_.model_dump()).returning(self.model)
            )
            res = await self.session.execute(add_data_statement)
            model = res.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.error(f"Не удалось добавить данные в БД, тип ошибки:{type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExsistExc from ex
            else:
                logging.error("Незнакомая ошибка")
                raise ex

    async def add_bulk(self, data_: list[BaseModel]):
        add_data_statement = insert(self.model).values(
            [item.model_dump() for item in data_]
        )
        await self.session.execute(add_data_statement)

    async def del_(self, **filter_by) -> None:
        delete_obj = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_obj)

    async def edit_(self, data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        edit_obj = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(edit_obj)
