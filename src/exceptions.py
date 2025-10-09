
class AppExc(Exception):
    detail = "Неожиданная ошибка"

    def __int__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class ObjectNotFoundExc(AppExc):
    detail = "Объект не найден"

class RoomCannotBeBookedExc(AppExc):
    detail = "Не осталось свободных номеров"
