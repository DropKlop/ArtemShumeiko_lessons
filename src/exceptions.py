from datetime import date

from fastapi import HTTPException


class AppExc(Exception):
    detail = "Неожиданная ошибка"

    def __int__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundExc(AppExc):
    detail = "Объект не найден"

class RoomCannotBeBookedExc(AppExc):
    detail = "Не осталось свободных номеров"

class ObjectAlreadyExsistExc(AppExc):
    detail = "Объект уже существует"


class AppHTTPExc(HTTPException):
    status_code = 500
    detail= None

    def __int__(self, *args, **kwargs):
        super().__init__(status_code= self.status_code, detail=self.detail)


class HotelNotFoundHTTPEx(AppHTTPExc):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPEx(AppHTTPExc):
    status_code = 404
    detail = "Номер не найден"


def check_date(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата заезда позже даты выезда")
