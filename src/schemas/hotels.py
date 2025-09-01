from pydantic import BaseModel, Field

# описание класса отель
class Hotel(BaseModel):
    title: str
    location: str

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)