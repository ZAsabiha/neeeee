import os
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

import models
from models import User, Event, Registration, init_engine, create_db_and_tables

from dotenv import load_dotenv
load_dotenv()


# ---------- DATABASE SETUP ----------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

init_engine(DATABASE_URL)


def get_session():
    with Session(models.engine) as session:
        yield session


# ---------- FASTAPI APP ----------
app = FastAPI(title="EventFinder API")


@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "EventFinder API is running"}

# ---------- USERS ----------
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # Prevent duplicate email
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# ---------- EVENTS ----------
@app.post("/events/", response_model=Event)
def create_event(event: Event, session: Session = Depends(get_session)):
    # Check that organizer exists
    organizer = session.get(User, event.organizer_id)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.get("/events/", response_model=List[Event])
def list_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, updated: Event, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.name = updated.name
    event.description = updated.description
    event.location = updated.location
    event.organizer_id = updated.organizer_id

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.delete("/events/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(event)
    session.commit()
    return {"message": "Event deleted"}


# ---------- REGISTRATION ----------
@app.post("/events/{event_id}/register", response_model=Registration)
def register(event_id: int, user_id: int, session: Session = Depends(get_session)):

    # Check event and user exist
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent duplicate registration
    exists = session.exec(
        select(Registration).where(
            Registration.event_id == event_id,
            Registration.user_id == user_id
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Already registered")

    reg = Registration(event_id=event_id, user_id=user_id)
    session.add(reg)
    session.commit()
    session.refresh(reg)

    return reg


@app.delete("/events/{event_id}/register")
def cancel_register(event_id: int, user_id: int, session: Session = Depends(get_session)):
    reg = session.exec(
        select(Registration).where(
            Registration.event_id == event_id,
            Registration.user_id == user_id
        )
    ).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(reg)
    session.commit()
    return {"message": "Registration canceled"}


@app.get("/events/{event_id}/attendees", response_model=List[User])
def attendees(event_id: int, session: Session = Depends(get_session)):
    registrations = session.exec(
        select(Registration).where(Registration.event_id == event_id)
    ).all()

    user_ids = [r.user_id for r in registrations]
    if not user_ids:
        return []

    return session.exec(select(User).where(User.id.in_(user_ids))).all()


@app.get("/users/{user_id}/registrations", response_model=List[Event])
def user_registrations(user_id: int, session: Session = Depends(get_session)):
    registrations = session.exec(
        select(Registration).where(Registration.user_id == user_id)
    ).all()

    event_ids = [r.event_id for r in registrations]
    if not event_ids:
        return []

    return session.exec(select(Event).where(Event.id.in_(event_ids))).all()
