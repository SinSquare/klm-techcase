"""Utils"""

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine
import os


def get_session():
    engine_kwargs = {"connect_args": {"connect_timeout": 10}}
    engine = create_engine(os.environ.get("DB_URL"), **engine_kwargs)
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
