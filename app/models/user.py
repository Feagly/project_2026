from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    """Campi comuni dell'utente, condivisi tra modello DB e schemi pubblici."""
    name: str
    email: str


class User(BaseUser, table=True):
    """Modello ORM per la tabella `user`. Lo username è la chiave primaria,
    fornita obbligatoriamente dal client alla creazione."""
    username: str = Field(primary_key=True)


class UserCreate(BaseUser):
    """Schema per creare un nuovo utente. Include lo username perché deve
    essere fornito dal client (è la chiave primaria)."""
    username: str

class UserPublic(BaseUser):
    """Schema di risposta pubblico per l'utente."""
    username: str