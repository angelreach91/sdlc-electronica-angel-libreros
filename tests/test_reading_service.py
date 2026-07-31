from datetime import datetime, timezone

import pytest

from app.models.reading import Reading
from app.services.reading_service import ReadingService

FIXED_TIME = datetime(2026, 7, 29, 18, 0, tzinfo=timezone.utc)
RANGE_START = datetime(2026, 7, 28, tzinfo=timezone.utc)
RANGE_END = datetime(2026, 7, 29, tzinfo=timezone.utc)


class FakeReadingRepository:
    """Repositorio en memoria utilizado únicamente durante las pruebas."""

    def __init__(self) -> None:
        self.readings: list[Reading] = []
        self._next_id = 1

    def add(self, reading: Reading) -> Reading:
        reading.id = self._next_id
        self._next_id += 1
        self.readings.append(reading)
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
        result = [
            reading
            for reading in self.readings
            if reading.sensor_id == sensor_id
            and (from_date is None or reading.received_at >= from_date)
            and (to_date is None or reading.received_at <= to_date)
        ]
        result.sort(key=lambda reading: (reading.received_at, reading.id))
        return result[offset : offset + limit]

    def get_by_id(self, reading_id: int) -> Reading | None:
        return next(
            (reading for reading in self.readings if reading.id == reading_id),
            None,
        )

    def update(self, reading: Reading) -> Reading:
        return reading

    def delete(self, reading: Reading) -> None:
        self.readings.remove(reading)


TestContext = tuple[ReadingService, FakeReadingRepository]


def fixed_clock() -> datetime:
    return FIXED_TIME


@pytest.fixture
def context() -> TestContext:
    repository = FakeReadingRepository()
    return ReadingService(repository, clock=fixed_clock), repository


def create_reading(service: ReadingService) -> Reading:
    return service.create_reading(
        sensor_id="sensor-01",
        temperature=24.5,
        humidity=60.0,
    )


def store_reading(
    repository: FakeReadingRepository,
    *,
    day: int,
    sensor_id: str = "sensor-01",
) -> Reading:
    return repository.add(
        Reading(
            sensor_id=sensor_id,
            temperature=20.0,
            humidity=50.0,
            received_at=datetime(2026, 7, day, tzinfo=timezone.utc),
        )
    )


def test_create_reading_stores_valid_data(context: TestContext) -> None:
    service, repository = context

    reading = service.create_reading(
        sensor_id=" sensor-01 ",
        temperature=24.5,
        humidity=60.0,
    )

    assert reading.id == 1
    assert reading.sensor_id == "sensor-01"
    assert reading.temperature == 24.5
    assert reading.humidity == 60.0
    assert reading.received_at == FIXED_TIME
    assert repository.readings == [reading]


@pytest.mark.parametrize(
    ("sensor_id", "temperature", "humidity", "message"),
    [
        ("   ", 24.5, 60.0, "sensor_id no puede estar vacío"),
        ("sensor-01", -273.16, 60.0, "temperature no puede ser menor"),
        ("sensor-01", 24.5, -0.1, "humidity debe estar entre 0 y 100"),
        ("sensor-01", 24.5, 100.1, "humidity debe estar entre 0 y 100"),
    ],
)
def test_create_reading_rejects_invalid_data(
    context: TestContext,
    sensor_id: str,
    temperature: float,
    humidity: float,
    message: str,
) -> None:
    service, repository = context

    with pytest.raises(ValueError, match=message):
        service.create_reading(sensor_id, temperature, humidity)

    assert repository.readings == []


def test_list_by_sensor_applies_filters_and_pagination(
    context: TestContext,
) -> None:
    service, repository = context

    store_reading(repository, day=27)
    store_reading(repository, day=28, sensor_id="sensor-02")
    first = store_reading(repository, day=28)
    second = store_reading(repository, day=29)
    store_reading(repository, day=30)

    filtered = service.list_by_sensor(
        " sensor-01 ",
        from_date=RANGE_START,
        to_date=RANGE_END,
    )
    page = service.list_by_sensor(
        "sensor-01",
        limit=1,
        offset=1,
        from_date=RANGE_START,
        to_date=RANGE_END,
    )

    assert filtered == [first, second]
    assert page == [second]


@pytest.mark.parametrize(
    ("limit", "offset", "from_date", "to_date", "message"),
    [
        (0, 0, None, None, "limit debe estar entre 1 y 100"),
        (101, 0, None, None, "limit debe estar entre 1 y 100"),
        (50, -1, None, None, "offset no puede ser negativo"),
        (
            50,
            0,
            RANGE_END,
            RANGE_START,
            "from_date no puede ser posterior a to_date",
        ),
    ],
)
def test_list_by_sensor_rejects_invalid_arguments(
    context: TestContext,
    limit: int,
    offset: int,
    from_date: datetime | None,
    to_date: datetime | None,
    message: str,
) -> None:
    service, _ = context

    with pytest.raises(ValueError, match=message):
        service.list_by_sensor(
            "sensor-01",
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )


def test_get_by_id_handles_existing_and_missing(
    context: TestContext,
) -> None:
    service, _ = context
    reading = create_reading(service)

    assert service.get_by_id(reading.id) is reading
    assert service.get_by_id(999) is None


def test_update_reading_handles_existing_and_missing(
    context: TestContext,
) -> None:
    service, _ = context
    reading = create_reading(service)

    result = service.update_reading(reading.id, temperature=26.0)

    assert result is reading
    assert reading.temperature == 26.0
    assert reading.humidity == 60.0
    assert service.update_reading(999, temperature=25.0) is None


def test_update_reading_rejects_empty_update(
    context: TestContext,
) -> None:
    service, _ = context

    with pytest.raises(
        ValueError,
        match="debe proporcionar al menos un valor",
    ):
        service.update_reading(1)


def test_delete_reading_handles_existing_and_missing(
    context: TestContext,
) -> None:
    service, repository = context
    reading = create_reading(service)

    assert service.delete_reading(reading.id) is True
    assert repository.readings == []
    assert service.delete_reading(reading.id) is False