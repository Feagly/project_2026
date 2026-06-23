from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.models.registration import Registration
from app.models.user import User
from app.models.event import Event
from app.data.db import SessionDep
from typing import Annotated

router = APIRouter(prefix="/registrations")


@router.get("/")
def get_all_registrations(session: SessionDep) -> list[Registration]:
    """Restituisce la lista di tutte le registrazioni esistenti."""
    return session.exec(select(Registration)).all()


@router.delete("/")
def delete_registration(
        session: SessionDep,
        username: Annotated[str, Query(description="Username of the registered user")],
        event_id: Annotated[int, Query(description="ID of the event")]
):
    """Elimina la registrazione dell'utente all'evento indicati."""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    registration = session.get(Registration, (username, event_id))
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    session.delete(registration)
    session.commit()
    return "Registration successfully deleted"