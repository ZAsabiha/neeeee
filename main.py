# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.routers import auth, events, users


app = FastAPI(title="EventFinder API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "EventFinder API is running"}


# ---------- INCLUDE ROUTERS ----------
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
