from pydantic import BaseModel

class EventCreate(BaseModel):
    name: str
    description: str
    location: str


class EventPublic(BaseModel):
    id: int
    name: str
    description: str
    location: str
    organizer_id: int

    class Config:
        from_attributes = True