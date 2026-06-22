from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.event import Event, EventPublic
from app.data.db import SessionDep

router = APIRouter(prefix="/events")


@router.get("/")
def get_all_events(session: SessionDep) -> list[EventPublic]:
    """Restituisce la lista di tutti gli eventi esistenti."""
    return session.exec(select(Event)).all()