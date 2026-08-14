from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertRepository(Protocol):
    """Define las operaciones de persistencia requeridas para alertas."""

    def add(self, alert: Alert) -> Alert:
        """Almacena y devuelve una alerta."""
        ...

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        """Consulta las alertas de un sensor."""
        ...


class SQLAlchemyAlertRepository:
    """Implementa AlertRepository mediante SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, alert: Alert) -> Alert:
        try:
            self._session.add(alert)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(alert)
        return alert

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        statement = select(Alert).where(Alert.sensor_id == sensor_id)
        return list(self._session.scalars(statement).all())
