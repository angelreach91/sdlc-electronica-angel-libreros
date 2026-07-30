from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.reading import Reading


class ReadingRepository(Protocol):
    """Define las operaciones de persistencia requeridas por el servicio."""

    def add(self, reading: Reading) -> Reading:
        """Almacena y devuelve una lectura."""
        ...

    def list_by_sensor(self, sensor_id: str) -> list[Reading]:
        """Devuelve las lecturas pertenecientes a un sensor."""
        ...


class SQLAlchemyReadingRepository:
    """Implementa ReadingRepository mediante una sesión de SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, reading: Reading) -> Reading:
        try:
            self._session.add(reading)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(reading)
        return reading

    def list_by_sensor(self, sensor_id: str) -> list[Reading]:
        statement = (
            select(Reading)
            .where(Reading.sensor_id == sensor_id)
            .order_by(Reading.received_at.asc(), Reading.id.asc())
        )
        return list(self._session.scalars(statement).all())