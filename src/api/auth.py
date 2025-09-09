
from fastapi import APIRouter, HTTPException, Response, Request

from src.repos.users import UsersRepository
from src.database import async_sessionmaker_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_sessionmaker_maker() as session:
        await UsersRepository(session).add_(new_user_data)
        await session.commit()
    return {"status":"OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_sessionmaker_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code = 401, detail="Пользователь с таким email не зареган")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
    return {"access_token":access_token}


@router.post("/login_auth")
async def only_auth(
        request: Request
):
    token = request.cookies.get("access_token")
    if token:
        return {"Access-token":token}
    else:
        raise HTTPException(status_code=404, detail="Токен не найден")