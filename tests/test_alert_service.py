from datetime import datetime

from app.models.alert import Alert
from app.services.alert_service import AlertService


class FakeAlertRepository:
    """Repositorio controlado para consultar alertas por sensor."""

    def __init__(self, alerts: list[Alert]) -> None:
        self.alerts = alerts
        self.list_arguments: list[str] = []

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        self.list_arguments.append(sensor_id)
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


def test_list_by_sensor_delegates_received_sensor_id() -> None:
    repository = FakeAlertRepository([])
    service = AlertService(repository)

    service.list_by_sensor("TEMP-01")

    assert repository.list_arguments == ["TEMP-01"]


def test_list_by_sensor_returns_repository_alerts() -> None:
    expected = [make_alert()]
    repository = FakeAlertRepository(expected)
    service = AlertService(repository)

    result = service.list_by_sensor("TEMP-01")

    assert result == expected
