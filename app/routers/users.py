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

@router.post("/")
def add_user(new_user: UserCreate, session: SessionDep):
    """Crea un nuovo utente, errore se lo username esiste già."""
    user = session.get(User, new_user.username)
    if user:
        raise HTTPException(status_code=409, detail="Username already exists")
    session.add(User.model_validate(new_user))
    session.commit()
    return "User successfully added"