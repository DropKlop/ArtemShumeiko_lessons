from pydantic import BaseModel, Field


class FacilitiesAdd(BaseModel):
    title: str

class Facilities(FacilitiesAdd):
    id: int