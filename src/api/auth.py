from fastapi import APIRouter
from passlib.context import CryptContext


from src.repos.users import UsersRepository
from src.database import async_sessionmaker_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_sessionmaker_maker() as session:
        await UsersRepository(session).add_(new_user_data)
        await session.commit()
    return {"status":"OK"}