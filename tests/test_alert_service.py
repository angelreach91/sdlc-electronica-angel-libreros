from datetime import datetime

import pytest

from app.alert_status import AlertStatus
from app.models.alert import Alert
from app.services.alert_service import AlertService


class FakeAlertRepository:
    """Repositorio controlado para consultar alertas por sensor."""

    def __init__(self, alerts: list[Alert]) -> None:
        self.alerts = alerts
        self.update_calls: list[Alert] = []
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

    def get_by_id(self, alert_id: int) -> Alert | None:
        return next(
            (alert for alert in self.alerts if alert.id == alert_id),
            None,
        )

    def update(self, alert: Alert) -> Alert:
        self.update_calls.append(alert)
        return alert

    def list_active(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Alert]:
        active_statuses = {
            AlertStatus.OPEN.value,
            AlertStatus.ACKNOWLEDGED.value,
        }
        return [
            alert
            for alert in self.alerts[offset:offset + limit]
            if alert.status in active_statuses
        ]


def make_alert(
    *,
    alert_id: int = 1,
    status: AlertStatus = AlertStatus.OPEN,
) -> Alert:
    """Construye una alerta representativa para el servicio."""

    return Alert(
        id=alert_id,
        sensor_id="TEMP-01",
        reading_id=42,
        value=31.5,
        threshold=30.0,
        created_at=datetime(2026, 8, 14, 10, 1),
        status=status.value,
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


def test_get_by_id_returns_requested_alert() -> None:
    expected = make_alert(alert_id=7)
    service = AlertService(FakeAlertRepository([expected]))

    result = service.get_by_id(7)

    assert result is expected


def test_get_by_id_returns_none_for_unknown_alert() -> None:
    service = AlertService(FakeAlertRepository([]))

    assert service.get_by_id(99) is None


def test_update_status_changes_open_to_acknowledged_and_persists() -> None:
    alert = make_alert(status=AlertStatus.OPEN)
    repository = FakeAlertRepository([alert])
    service = AlertService(repository)

    result = service.update_status(1, AlertStatus.ACKNOWLEDGED)

    assert result is alert
    assert alert.status == AlertStatus.ACKNOWLEDGED.value
    assert repository.update_calls == [alert]


def test_update_status_changes_acknowledged_to_resolved_and_persists() -> None:
    alert = make_alert(status=AlertStatus.ACKNOWLEDGED)
    repository = FakeAlertRepository([alert])
    service = AlertService(repository)

    result = service.update_status(1, AlertStatus.RESOLVED)

    assert result is alert
    assert alert.status == AlertStatus.RESOLVED.value
    assert repository.update_calls == [alert]


def test_update_status_returns_none_for_unknown_alert() -> None:
    repository = FakeAlertRepository([])
    service = AlertService(repository)

    assert service.update_status(99, AlertStatus.ACKNOWLEDGED) is None
    assert repository.update_calls == []


@pytest.mark.parametrize(
    ("current", "requested"),
    [
        (AlertStatus.OPEN, AlertStatus.OPEN),
        (AlertStatus.OPEN, AlertStatus.RESOLVED),
        (AlertStatus.ACKNOWLEDGED, AlertStatus.OPEN),
        (AlertStatus.ACKNOWLEDGED, AlertStatus.ACKNOWLEDGED),
        (AlertStatus.RESOLVED, AlertStatus.OPEN),
        (AlertStatus.RESOLVED, AlertStatus.ACKNOWLEDGED),
        (AlertStatus.RESOLVED, AlertStatus.RESOLVED),
    ],
)
def test_update_status_rejects_invalid_transition(
    current: AlertStatus,
    requested: AlertStatus,
) -> None:
    alert = make_alert(status=current)
    repository = FakeAlertRepository([alert])
    service = AlertService(repository)

    with pytest.raises(
        ValueError,
        match=f"{current.value}.*{requested.value}",
    ):
        service.update_status(1, requested)

    assert alert.status == current.value
    assert repository.update_calls == []


def test_list_active_returns_only_open_and_acknowledged_alerts() -> None:
    open_alert = make_alert(alert_id=1, status=AlertStatus.OPEN)
    acknowledged_alert = make_alert(
        alert_id=2,
        status=AlertStatus.ACKNOWLEDGED,
    )
    resolved_alert = make_alert(
        alert_id=3,
        status=AlertStatus.RESOLVED,
    )
    service = AlertService(
        FakeAlertRepository(
            [open_alert, acknowledged_alert, resolved_alert]
        )
    )

    result = service.list_active()

    assert result == [open_alert, acknowledged_alert]
    assert resolved_alert not in result


@pytest.mark.parametrize("alert_id", [0, -1])
def test_alert_operations_reject_non_positive_id(alert_id: int) -> None:
    service = AlertService(FakeAlertRepository([]))

    with pytest.raises(
        ValueError,
        match="alert_id debe ser mayor que cero",
    ):
        service.get_by_id(alert_id)

    with pytest.raises(
        ValueError,
        match="alert_id debe ser mayor que cero",
    ):
        service.update_status(alert_id, AlertStatus.ACKNOWLEDGED)
