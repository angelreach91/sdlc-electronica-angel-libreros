from datetime import datetime
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.reading import Reading


class ReadingRepository(Protocol):
    """Define las operaciones de persistencia requeridas por el servicio."""

    def add(self, reading: Reading) -> Reading:
        """Almacena y devuelve una lectura."""
        ...

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Reading]:
        """Consulta las lecturas de un sensor aplicando filtros y paginación."""
        ...

    def get_by_id(self, reading_id: int) -> Reading | None:
        """Busca una lectura mediante su identificador."""
        ...

    def get_statistics_by_sensor(
        self,
        sensor_id: str,
        *,
        from_date: datetime,
        to_date: datetime,
    ) -> tuple[float, float, float] | None:
        """Calcula mínimo, máximo y promedio para un período."""
        ...

    def update(self, reading: Reading) -> Reading:
        """Confirma y devuelve los cambios de una lectura."""
        ...

    def delete(self, reading: Reading) -> None:
        """Elimina una lectura almacenada."""
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

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Reading]:
        statement = select(Reading).where(Reading.sensor_id == sensor_id)

        if from_date is not None:
            statement = statement.where(Reading.received_at >= from_date)

        if to_date is not None:
            statement = statement.where(Reading.received_at <= to_date)

        statement = statement.order_by(
            Reading.received_at.asc(),
            Reading.id.asc(),
        ).limit(limit).offset(offset)

        return list(self._session.scalars(statement).all())

    def get_by_id(self, reading_id: int) -> Reading | None:
        statement = select(Reading).where(Reading.id == reading_id)
        return self._session.scalar(statement)

    def get_statistics_by_sensor(
        self,
        sensor_id: str,
        *,
        from_date: datetime,
        to_date: datetime,
    ) -> tuple[float, float, float] | None:
        statement = select(
            func.min(Reading.value),
            func.max(Reading.value),
            func.avg(Reading.value),
            func.count(Reading.id),
        ).where(
            Reading.sensor_id == sensor_id,
            Reading.received_at >= from_date,
            Reading.received_at <= to_date,
        )
        minimum, maximum, average, count = self._session.execute(
            statement
        ).one()

        if count == 0:
            return None

        return (
            float(minimum),
            float(maximum),
            float(average),
        )

    def update(self, reading: Reading) -> Reading:
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(reading)
        return reading

    def delete(self, reading: Reading) -> None:
        try:
            self._session.delete(reading)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise
