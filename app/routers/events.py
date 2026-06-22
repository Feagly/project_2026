from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select
from app.models.event import Event, EventPublic, EventCreate
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

@router.post("/")
def add_event(event: EventCreate, session: SessionDep):
    """Crea un nuovo evento e lo salva nel database."""
    session.add(Event.model_validate(event))
    session.commit()
    return "Event successfully added"

@router.put("/{id}")
def update_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to update")],
        new_event: EventCreate
):
    """Aggiorna l'evento con l'id indicato con i nuovi dati forniti."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.title = new_event.title
    event.description = new_event.description
    event.date = new_event.date
    event.location = new_event.location
    session.add(event)
    session.commit()
    return "Event successfully updated"