from datetime import datetime
from typing import Protocol

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
