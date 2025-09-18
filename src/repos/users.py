from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repos.base import BaseRepository
from src.repos.mapper.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        select_query = select(self.model).filter_by(email=email)
        res = await self.session.execute(select_query)
        model = res.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
