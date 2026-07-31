from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.reading_repository import SQLAlchemyReadingRepository
from app.services.reading_service import ReadingService


def get_session() -> Generator[Session, None, None]:
    """Proporciona una sesión de SQLAlchemy durante una petición."""

    with SessionLocal() as session:
        yield session


def get_reading_service(
    session: Annotated[Session, Depends(get_session)],
) -> ReadingService:
    """Construye el servicio con el repositorio de SQLAlchemy."""

    repository = SQLAlchemyReadingRepository(session)
    return ReadingService(repository)