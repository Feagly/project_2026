from fastapi import APIRouter
from sqlmodel import select
from app.models.registration import Registration
from app.data.db import SessionDep

router = APIRouter(prefix="/registrations")

@router.get("/")
def get_all_registrations(session: SessionDep) -> list[Registration]:
    """Restituisce la lista di tutte le registrazioni esistenti."""
    return session.exec(select(Registration)).all()