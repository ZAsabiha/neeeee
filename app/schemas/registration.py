from pydantic import BaseModel

# ---------- REGISTRATION ----------

class RegistrationPublic(BaseModel):
    id: int
    user_id: int
    event_id: int

    class Config:
        from_attributes = True
