from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.alert_status import AlertStatus
from app.dependencies import get_alert_service
from app.main import app
from app.models.alert import Alert

FIXED_TIME = datetime(2026, 8, 21, 12, 0, tzinfo=timezone.utc)


def make_alert(
    *,
    alert_id: int,
    status: AlertStatus,
) -> Alert:
    """Construye una alerta controlada para las pruebas HTTP."""

    return Alert(
        id=alert_id,
        sensor_id="TEMP-01",
        reading_id=42,
        value=31.5,
        threshold=30.0,
        created_at=FIXED_TIME,
        status=status.value,
    )


class FakeAlertService:
    """Servicio controlado utilizado para probar el router de alertas."""

    def __init__(self) -> None:
        self.active_alerts = [
            make_alert(alert_id=1, status=AlertStatus.OPEN),
            make_alert(alert_id=2, status=AlertStatus.ACKNOWLEDGED),
        ]
        self.update_result: Alert | None = make_alert(
            alert_id=1,
            status=AlertStatus.ACKNOWLEDGED,
        )
        self.update_error: ValueError | None = None
        self.update_arguments: tuple[int, AlertStatus] | None = None

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        return self.active_alerts[offset:offset + limit]

    def update_status(
        self,
        alert_id: int,
        status: AlertStatus,
    ) -> Alert | None:
        self.update_arguments = (alert_id, status)

        if self.update_error is not None:
            raise self.update_error

        return self.update_result


@contextmanager
def alert_client(
    service: FakeAlertService,
) -> Generator[TestClient, None, None]:
    """Proporciona un cliente con el servicio de alertas sustituido."""

    app.dependency_overrides[get_alert_service] = lambda: service

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_alert_service, None)


def test_list_active_alerts_returns_open_and_acknowledged() -> None:
    service = FakeAlertService()

    with alert_client(service) as client:
        response = client.get("/alerts/active")

    assert response.status_code == 200
    assert [alert["status"] for alert in response.json()] == [
        "open",
        "acknowledged",
    ]


def test_update_alert_status_returns_updated_alert() -> None:
    service = FakeAlertService()

    with alert_client(service) as client:
        response = client.patch(
            "/alerts/1/status",
            json={"status": "acknowledged"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"
    assert service.update_arguments == (1, AlertStatus.ACKNOWLEDGED)


def test_update_alert_status_returns_404_for_unknown_alert() -> None:
    service = FakeAlertService()
    service.update_result = None

    with alert_client(service) as client:
        response = client.patch(
            "/alerts/999/status",
            json={"status": "acknowledged"},
        )

    assert response.status_code == 404


def test_update_alert_status_rejects_unknown_status_with_422() -> None:
    service = FakeAlertService()

    with alert_client(service) as client:
        response = client.patch(
            "/alerts/1/status",
            json={"status": "closed"},
        )

    assert response.status_code == 422
    assert service.update_arguments is None


def test_update_alert_status_translates_invalid_transition_to_400() -> None:
    service = FakeAlertService()
    service.update_error = ValueError(
        "transición de alerta inválida: open -> resolved"
    )

    with alert_client(service) as client:
        response = client.patch(
            "/alerts/1/status",
            json={"status": "resolved"},
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "transición de alerta inválida: open -> resolved"
    }
