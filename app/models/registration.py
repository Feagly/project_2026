from sqlmodel import Field, SQLModel


class Registration(SQLModel, table=True):
    # Chiave primaria composta (username, event_id):
    # garantisce che un utente non possa registrarsi due volte allo stesso evento
    username: str = Field(foreign_key="user.username", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)