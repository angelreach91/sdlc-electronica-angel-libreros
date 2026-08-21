from datetime import datetime
from typing import Protocol

from app.alert_status import AlertStatus
from app.models.alert import Alert


class AlertQueryRepository(Protocol):
    """Define las operaciones requeridas para consultar alertas."""

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Alert]:
        """Consulta alertas de un sensor con filtros y paginación."""
        ...

    def get_by_id(self, alert_id: int) -> Alert | None:
        """Busca una alerta mediante su identificador."""
        ...

    def update(self, alert: Alert) -> Alert:
        """Persiste los cambios de una alerta."""
        ...

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        """Consulta las alertas abiertas o reconocidas."""
        ...


class AlertService:
    """Consulta las alertas generadas para los sensores."""

    def __init__(self, repository: AlertQueryRepository) -> None:
        self._repository = repository

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Alert]:
        """Devuelve alertas aplicando filtros y paginación."""

        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")

        if offset < 0:
            raise ValueError("offset no puede ser negativo")

        if from_date is not None and to_date is not None:
            from_date_is_aware = from_date.utcoffset() is not None
            to_date_is_aware = to_date.utcoffset() is not None

            if from_date_is_aware != to_date_is_aware:
                raise ValueError(
                    "from_date y to_date deben tener la misma "
                    "conciencia de zona horaria"
                )

            if from_date > to_date:
                raise ValueError(
                    "from_date no puede ser posterior a to_date"
                )

        return self._repository.list_by_sensor(
            sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    def get_by_id(self, alert_id: int) -> Alert | None:
        """Busca una alerta mediante su identificador."""

        self._validate_alert_id(alert_id)
        return self._repository.get_by_id(alert_id)

    def update_status(
        self,
        alert_id: int,
        status: AlertStatus,
    ) -> Alert | None:
        """Avanza una alerta al siguiente estado permitido."""

        self._validate_alert_id(alert_id)
        alert = self._repository.get_by_id(alert_id)

        if alert is None:
            return None

        current_status = AlertStatus(alert.status)
        valid_transitions = {
            (AlertStatus.OPEN, AlertStatus.ACKNOWLEDGED),
            (AlertStatus.ACKNOWLEDGED, AlertStatus.RESOLVED),
        }

        if (current_status, status) not in valid_transitions:
            raise ValueError(
                "transición de alerta inválida: "
                f"{current_status.value} -> {status.value}"
            )

        alert.status = status.value
        return self._repository.update(alert)

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        """Devuelve las alertas abiertas o reconocidas."""

        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")

        if offset < 0:
            raise ValueError("offset no puede ser negativo")

        return self._repository.list_active(
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def _validate_alert_id(alert_id: int) -> None:
        if alert_id <= 0:
            raise ValueError("alert_id debe ser mayor que cero")
