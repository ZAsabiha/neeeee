from __future__ import annotations

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Registration(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")

    # attendee: "User" = Relationship(back_populates="registrations")
    # event: "Event" = Relationship(back_populates="registrations")
