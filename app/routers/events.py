from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from app.models.event import Event, EventPublic
from app.data.db import SessionDep
from typing import Annotated

router = APIRouter(prefix="/events")


@router.get("/")
def get_all_events(session: SessionDep) -> list[EventPublic]:
    """Restituisce la lista di tutti gli eventi esistenti."""
    return session.exec(select(Event)).all()

@router.get("/{id}")
def get_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to get")]
) -> EventPublic:
    """Restituisce l'evento con l'id indicato, o 404 se non esiste."""
    event = session.get(Event, id)
    if event:
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")