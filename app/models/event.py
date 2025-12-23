from __future__ import annotations

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location: str

    # organizer_id: int = Field(foreign_key="user.id")
    # organizer: "User" = Relationship(back_populates="events_organized")

    # registrations: List["Registration"] = Relationship(back_populates="event")
