from pydantic import BaseModel


# ---------- USERS ----------

class UserCreate(BaseModel):
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  # Pydantic v2; use orm_mode=True in v1