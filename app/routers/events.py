from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import get_current_user
from app.models import User, Event, Registration
from app.schemas import (
    EventCreate,
    EventPublic,
    RegistrationPublic,
    UserPublic,
)

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


# ---------- EVENTS ----------

@router.post("/",
             response_model=EventPublic,
             status_code=status.HTTP_201_CREATED)
def create_event(
    event_in: EventCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Only logged-in users can create events
    event = Event(
        name=event_in.name,
        description=event_in.description,
        location=event_in.location,
        organizer_id=current_user.id,  # 🔐 from token
    )

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/", response_model=List[EventPublic])
def list_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@router.get("/{event_id}", response_model=EventPublic)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventPublic)
def update_event(
    event_id: int,
    updated: EventCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # (optional) check current_user.id == event.organizer_id
    event.name = updated.name
    event.description = updated.description
    event.location = updated.location

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # (optional) check organizer
    session.delete(event)
    session.commit()
    return {"message": "Event deleted"}


# ---------- REGISTRATIONS (protected) ----------

@router.post(
    "/{event_id}/register",
    response_model=RegistrationPublic,
    status_code=status.HTTP_201_CREATED,
)
def register_for_event(
    event_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    exists = session.exec(
        select(Registration).where(
            Registration.event_id == event_id,
            Registration.user_id == current_user.id,
        )
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Already registered")

    reg = Registration(event_id=event_id, user_id=current_user.id)  # 🔐 from token
    session.add(reg)
    session.commit()
    session.refresh(reg)
    return reg


@router.delete("/{event_id}/register")
def cancel_register(
    event_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    reg = session.exec(
        select(Registration).where(
            Registration.event_id == event_id,
            Registration.user_id == current_user.id,
        )
    ).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(reg)
    session.commit()
    return {"message": "Registration canceled"}


@router.get("/{event_id}/attendees", response_model=List[UserPublic])
def attendees(event_id: int, session: Session = Depends(get_session)):
    registrations = session.exec(
        select(Registration).where(Registration.event_id == event_id)
    ).all()

    user_ids = [r.user_id for r in registrations]
    if not user_ids:
        return []

    return session.exec(select(User).where(User.id.in_(user_ids))).all()
