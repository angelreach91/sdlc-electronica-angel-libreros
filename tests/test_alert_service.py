from datetime import datetime

import pytest

from app.models.alert import Alert
from app.services.alert_service import AlertService


class FakeAlertRepository:
    """Repositorio controlado para consultar alertas por sensor."""

    def __init__(self, alerts: list[Alert]) -> None:
        self.alerts = alerts
        self.list_arguments: list[
            tuple[
                str,
                int,
                int,
                datetime | None,
                datetime | None,
            ]
        ] = []

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Alert]:
        self.list_arguments.append(
            (sensor_id, limit, offset, from_date, to_date)
        )
        return self.alerts


def make_alert() -> Alert:
    """Construye una alerta representativa para el servicio."""

    return Alert(
        id=1,
        sensor_id="TEMP-01",
        reading_id=42,
        value=31.5,
        threshold=30.0,
        created_at=datetime(2026, 8, 14, 10, 1),
    )


def test_list_by_sensor_delegates_filters_and_pagination() -> None:
    repository = FakeAlertRepository([])
    service = AlertService(repository)
    from_date = datetime(2026, 8, 14, 10, 0)
    to_date = datetime(2026, 8, 14, 11, 0)

    service.list_by_sensor(
        "TEMP-01",
        limit=20,
        offset=5,
        from_date=from_date,
        to_date=to_date,
    )

    assert repository.list_arguments == [
        ("TEMP-01", 20, 5, from_date, to_date)
    ]


def test_list_by_sensor_returns_repository_alerts() -> None:
    expected = [make_alert()]
    repository = FakeAlertRepository(expected)
    service = AlertService(repository)

    result = service.list_by_sensor("TEMP-01")

    assert result == expected


@pytest.mark.parametrize("limit", [0, 101])
def test_list_by_sensor_rejects_invalid_limit(limit: int) -> None:
    service = AlertService(FakeAlertRepository([]))

    with pytest.raises(ValueError, match="limit debe estar entre 1 y 100"):
        service.list_by_sensor("TEMP-01", limit=limit)


def test_list_by_sensor_rejects_negative_offset() -> None:
    service = AlertService(FakeAlertRepository([]))

    with pytest.raises(ValueError, match="offset no puede ser negativo"):
        service.list_by_sensor("TEMP-01", offset=-1)


def test_list_by_sensor_rejects_reversed_date_range() -> None:
    service = AlertService(FakeAlertRepository([]))

    with pytest.raises(
        ValueError,
        match="from_date no puede ser posterior a to_date",
    ):
        service.list_by_sensor(
            "TEMP-01",
            from_date=datetime(2026, 8, 15, 10, 0),
            to_date=datetime(2026, 8, 14, 10, 0),
        )
