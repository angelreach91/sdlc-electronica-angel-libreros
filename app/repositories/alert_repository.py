from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.alert_status import AlertStatus
from app.models.alert import Alert


class AlertRepository(Protocol):
    """Define las operaciones de persistencia requeridas para alertas."""

    def add(self, alert: Alert) -> Alert:
        """Almacena y devuelve una alerta."""
        ...

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Alert]:
        """Consulta alertas aplicando filtros y paginación."""
        ...

    def get_by_id(self, alert_id: int) -> Alert | None:
        """Busca una alerta mediante su identificador."""
        ...

    def update(self, alert: Alert) -> Alert:
        """Confirma y devuelve los cambios de una alerta."""
        ...

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        """Consulta las alertas abiertas o reconocidas."""
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

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Alert]:
        statement = select(Alert).where(Alert.sensor_id == sensor_id)

        if from_date is not None:
            statement = statement.where(Alert.created_at >= from_date)

        if to_date is not None:
            statement = statement.where(Alert.created_at <= to_date)

        statement = statement.order_by(
            Alert.created_at.asc(),
            Alert.id.asc(),
        ).limit(limit).offset(offset)

        return list(self._session.scalars(statement).all())

    def get_by_id(self, alert_id: int) -> Alert | None:
        statement = select(Alert).where(Alert.id == alert_id)
        return self._session.scalar(statement)

    def update(self, alert: Alert) -> Alert:
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        self._session.refresh(alert)
        return alert

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        statement = (
            select(Alert)
            .where(
                Alert.status.in_(
                    (
                        AlertStatus.OPEN.value,
                        AlertStatus.ACKNOWLEDGED.value,
                    )
                )
            )
            .order_by(
                Alert.created_at.asc(),
                Alert.id.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        return list(self._session.scalars(statement).all())
