# app/routers/users.py
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.database import get_session
from app.models import Registration, Event
from app.schemas import EventPublic


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}/registrations", response_model=List[EventPublic])
def user_registrations(user_id: int, session: Session = Depends(get_session)):
    registrations = session.exec(
        select(Registration).where(Registration.user_id == user_id)
    ).all()

    event_ids = [r.event_id for r in registrations]
    if not event_ids:
        return []

    return session.exec(select(Event).where(Event.id.in_(event_ids))).all()
