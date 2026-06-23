from fastapi import APIRouter, HTTPException, Path
from sqlmodel import select, delete
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

@router.get("/{username}")
def get_user(
        session: SessionDep,
        username: Annotated[str, Path(description="The username of the user to get")]
) -> UserPublic:
    """Restituisce l'utente con lo username indicato, o 404 se non esiste."""
    user = session.get(User, username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/")
def delete_all_users(session: SessionDep):
    """Elimina tutti gli utenti esistenti."""
    session.exec(delete(User))
    session.commit()
    return "All users successfully deleted"


@router.delete("/{username}")
def delete_user(
        session: SessionDep,
        username: Annotated[str, Path(description="The username of the user to delete")]
):
    """Elimina l'utente indicato, eliminando anche le registrazioni associate."""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    registrations = session.exec(
        select(Registration).where(Registration.username == username)
    ).all()
    for registration in registrations:
        session.delete(registration)

    session.delete(user)
    session.commit()
    return "User successfully deleted"