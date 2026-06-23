from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.models.event import Event, EventPublic, EventCreate
from app.models.user import User, UserCreate
from app.models.registration import Registration
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

@router.post("/{id}/register")
def register_user_to_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event")],
        user_data: UserCreate
):
    """Registra un utente all'evento. Crea l'utente se non esiste."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # crea l'utente se non esiste già
    user = session.get(User, user_data.username)
    if not user:
        session.add(User.model_validate(user_data))

    # crea la registrazione (se non già presente)
    existing = session.get(Registration, (user_data.username, id))
    if not existing:
        session.add(Registration(username=user_data.username, event_id=id))

    session.commit()
    return "User successfully registered to event"

@router.delete("/")
def delete_all_events(session: SessionDep):
    """Elimina tutti gli eventi esistenti."""
    session.exec(delete(Event))
    session.commit()
    return "All events successfully deleted"

@router.delete("/{id}")
def delete_event(
        session: SessionDep,
        id: Annotated[int, Path(description="The ID of the event to delete")]
):
    """Elimina l'evento con l'id indicato, eliminando anche le registrazioni associate."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    registrations = session.exec(
        select(Registration).where(Registration.event_id == id)
    ).all()
    for registration in registrations:
        session.delete(registration)

    session.delete(event)
    session.commit()
    return "Event successfully deleted"