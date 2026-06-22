from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    """Campi comuni dell'utente, condivisi tra modello DB e schema pubblico."""
    name: str
    email: str


class User(BaseUser, table=True):
    """Modello ORM per la tabella `user`. Username è la chiave primaria,
    fornita obbligatoriamente dal client alla creazione."""
    username: str = Field(primary_key=True)


class UserPublic(BaseUser):
    """Schema di risposta pubblico per l'utente."""
    username: str