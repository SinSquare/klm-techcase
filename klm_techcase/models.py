"""Request, response and DB models."""

from typing import Optional
from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class NoteInput(SQLModel):
    """Note input model"""

    text: str


class NoteOutput(NoteInput):
    """Note output model"""

    id: int


class Note(NoteInput, table=True):
    """Note DB model"""

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default=func.now(),
        nullable=False,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"onupdate": func.now()},
    )
