from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
from app.models.event import Event, EventPublic, EventCreate
from app.models.user import User, UserCreate, UserPublic
from app.models.registration import Registration
from app.data.db import SessionDep
from typing import Annotated

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Restituisce la lista di tutti gli utenti esistenti."""
    return session.exec(select(User)).all()