from sqlmodel import SQLModel, Field
from datetime import datetime


class BaseEvent(SQLModel):
    """Campi comuni dell'evento, condivisi tra modello DB e schema pubblico."""
    title: str
    description: str
    date: datetime
    location: str


class Event(BaseEvent, table=True):
    """Modello ORM per la tabella `event`. L'id è la chiave primaria,
    assegnata automaticamente dal database alla creazione."""
    id: int | None = Field(default=None, primary_key=True)


class EventPublic(BaseEvent):
    """Schema di risposta pubblico per l'evento."""
    id: int