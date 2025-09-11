from pydantic import BaseModel, Field

# описание класса комната
class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int

class RoomAdd(BaseModel):
    title: str
    hotel_id: int
    description: str | None = None
    price: int
    quantity: int


class Room(RoomAdd):
    id: int


class RoomPatch(BaseModel):
    title: str | None = None
    hotel_id: int | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None