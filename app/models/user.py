from __future__ import annotations

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    # Relationships
    # events_organized: List["Event"] = Relationship(back_populates="organizer")
    # registrations: List["Registration"] = Relationship(back_populates="attendee")
