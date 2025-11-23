from __future__ import annotations
from typing import Optional

from sqlmodel import SQLModel, Field, create_engine


# ---------- MODELS ----------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str = ""


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location: str

    # FK to User
    organizer_id: int = Field(foreign_key="user.id")


class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # FK to User and Event
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")


# ---------- DB ENGINE ----------

engine = None  # will be initialized from main.py


def init_engine(database_url: str):
    global engine
    if engine is None:
        engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    if engine is None:
        raise RuntimeError("Engine not initialized!")
    SQLModel.metadata.create_all(engine)
