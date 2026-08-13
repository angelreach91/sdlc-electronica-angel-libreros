from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.sensor import Sensor


class SensorLookupRepository(Protocol):
    """Define la consulta de sensores requerida por lecturas."""

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        """Busca un sensor mediante su identificador."""
        ...


class SensorRepository(Protocol):
    """Define las operaciones de persistencia requeridas para sensores."""

    def add(self, sensor: Sensor) -> Sensor:
        """Almacena y devuelve un sensor."""
        ...

    def list_all(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        """Consulta los sensores aplicando paginación."""
        ...

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        """Busca un sensor mediante su identificador."""
        ...

    def update(self, sensor: Sensor) -> Sensor:
        """Confirma y devuelve los cambios de un sensor."""
        ...


class SQLAlchemySensorRepository:
    """Implementa SensorRepository mediante SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, sensor: Sensor) -> Sensor:
        try:
            self._session.add(sensor)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(sensor)
        return sensor

    def list_all(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        statement = (
            select(Sensor)
            .order_by(Sensor.id.asc())
            .limit(limit)
            .offset(offset)
        )

        return list(self._session.scalars(statement).all())

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        statement = select(Sensor).where(Sensor.id == sensor_id)
        return self._session.scalar(statement)

    def update(self, sensor: Sensor) -> Sensor:
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(sensor)
        return sensor
