from dataclasses import dataclass
from datetime import datetime, timezone

from app.alert_status import AlertStatus
from app.models.alert import Alert
from app.models.reading import Reading
from app.services.anomaly_service import AnomalyService

FIXED_TIME = datetime(2026, 8, 13, 12, 0, tzinfo=timezone.utc)
SENSOR_ID = "TEMP-01"
READING_ID = 42
THRESHOLD = 30.0


@dataclass
class SensorWithThreshold:
    """Representación temporal de un sensor con threshold configurable."""

    id: str
    threshold: float | None


class FakeSensorRepository:
    """Repositorio controlado para consultar sensores por id."""

    def __init__(self, sensor: SensorWithThreshold) -> None:
        self.sensor = sensor
        self.get_arguments: list[str] = []

    def get_by_id(self, sensor_id: str) -> SensorWithThreshold | None:
        self.get_arguments.append(sensor_id)
        return self.sensor if self.sensor.id == sensor_id else None


class FakeAlertRepository:
    """Repositorio controlado que registra las alertas guardadas."""

    def __init__(self) -> None:
        self.add_calls: list[Alert] = []

    def add(self, alert: Alert) -> Alert:
        self.add_calls.append(alert)
        return alert


class FakeNotificationStrategy:
    """Estrategia sustituible que registra las alertas notificadas."""

    def __init__(self) -> None:
        self.notify_calls: list[Alert] = []

    def notify(self, alert: Alert) -> None:
        self.notify_calls.append(alert)


TestContext = tuple[
    AnomalyService,
    FakeSensorRepository,
    FakeAlertRepository,
    FakeNotificationStrategy,
]


def fixed_clock() -> datetime:
    return FIXED_TIME


def create_reading(value: float) -> Reading:
    """Representa una lectura que ya fue almacenada."""

    return Reading(
        id=READING_ID,
        sensor_id=SENSOR_ID,
        value=value,
        unit="C",
        received_at=datetime(2026, 8, 13, 11, 59, tzinfo=timezone.utc),
    )


def create_context(threshold: float | None) -> TestContext:
    sensor_repository = FakeSensorRepository(
        SensorWithThreshold(id=SENSOR_ID, threshold=threshold)
    )
    alert_repository = FakeAlertRepository()
    notification_strategy = FakeNotificationStrategy()
    service = AnomalyService(
        sensor_repository=sensor_repository,
        alert_repository=alert_repository,
        notification_strategy=notification_strategy,
        clock=fixed_clock,
    )

    return (
        service,
        sensor_repository,
        alert_repository,
        notification_strategy,
    )


def test_sensor_without_threshold_returns_none_without_saving_or_notifying(
) -> None:
    service, sensor_repository, alert_repository, notification_strategy = (
        create_context(threshold=None)
    )
    reading = create_reading(value=35.0)

    result = service.evaluate(reading)

    assert result is None
    assert sensor_repository.get_arguments == [SENSOR_ID]
    assert alert_repository.add_calls == []
    assert notification_strategy.notify_calls == []


def test_value_below_threshold_returns_none_without_saving_or_notifying(
) -> None:
    service, _, alert_repository, notification_strategy = create_context(
        threshold=THRESHOLD
    )
    reading = create_reading(value=29.9)

    result = service.evaluate(reading)

    assert result is None
    assert alert_repository.add_calls == []
    assert notification_strategy.notify_calls == []


def test_value_equal_to_threshold_returns_none_without_saving_or_notifying(
) -> None:
    service, _, alert_repository, notification_strategy = create_context(
        threshold=THRESHOLD
    )
    reading = create_reading(value=THRESHOLD)

    result = service.evaluate(reading)

    assert result is None
    assert alert_repository.add_calls == []
    assert notification_strategy.notify_calls == []


def test_value_above_threshold_creates_saves_and_returns_alert() -> None:
    service, _, alert_repository, _ = create_context(threshold=THRESHOLD)
    reading = create_reading(value=30.1)

    result = service.evaluate(reading)

    assert isinstance(result, Alert)
    assert alert_repository.add_calls == [result]


def test_created_alert_preserves_reading_threshold_and_clock_data() -> None:
    service, _, _, _ = create_context(threshold=THRESHOLD)
    reading = create_reading(value=31.5)

    alert = service.evaluate(reading)

    assert alert is not None
    assert alert.sensor_id == SENSOR_ID
    assert alert.reading_id == READING_ID
    assert alert.value == 31.5
    assert alert.threshold == THRESHOLD
    assert alert.created_at == FIXED_TIME


def test_value_above_threshold_creates_open_alert() -> None:
    service, _, alert_repository, _ = create_context(threshold=THRESHOLD)
    reading = create_reading(value=31.5)

    alert = service.evaluate(reading)

    assert alert is not None
    assert alert.status == AlertStatus.OPEN
    assert alert_repository.add_calls == [alert]


def test_created_alert_is_sent_to_injected_notification_strategy() -> None:
    service, _, _, notification_strategy = create_context(
        threshold=THRESHOLD
    )
    reading = create_reading(value=31.5)

    alert = service.evaluate(reading)

    assert alert is not None
    assert notification_strategy.notify_calls == [alert]
