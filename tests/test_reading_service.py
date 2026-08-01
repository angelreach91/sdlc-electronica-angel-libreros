from datetime import datetime, timezone

import pytest

from app.models.reading import Reading
from app.models.sensor import Sensor
from app.sensor_types import SensorUnit
from app.services.reading_service import ReadingService

FIXED_TIME = datetime(2026, 7, 31, 18, 0, tzinfo=timezone.utc)
RANGE_START = datetime(2026, 7, 28, tzinfo=timezone.utc)
RANGE_END = datetime(2026, 7, 29, tzinfo=timezone.utc)


class FakeReadingRepository:
    """Repositorio controlado utilizado para probar ReadingService."""

    def __init__(self) -> None:
        self.readings: list[Reading] = []
        self._next_id = 1

        self.add_calls: list[Reading] = []
        self.list_arguments: (
            tuple[
                str,
                int,
                int,
                datetime | None,
                datetime | None,
            ]
            | None
        ) = None
        self.list_result: list[Reading] = []
        self.get_arguments: list[int] = []
        self.update_calls: list[Reading] = []
        self.delete_calls: list[Reading] = []

    def add(self, reading: Reading) -> Reading:
        reading.id = self._next_id
        self._next_id += 1

        self.readings.append(reading)
        self.add_calls.append(reading)

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
        self.list_arguments = (
            sensor_id,
            limit,
            offset,
            from_date,
            to_date,
        )

        return self.list_result

    def get_by_id(self, reading_id: int) -> Reading | None:
        self.get_arguments.append(reading_id)

        return next(
            (
                reading
                for reading in self.readings
                if reading.id == reading_id
            ),
            None,
        )

    def update(self, reading: Reading) -> Reading:
        self.update_calls.append(reading)
        return reading

    def delete(self, reading: Reading) -> None:
        self.delete_calls.append(reading)
        self.readings.remove(reading)


class FakeSensorRepository:
    """Repositorio controlado de sensores."""

    def __init__(self) -> None:
        self.sensors: dict[str, Sensor] = {}
        self.get_arguments: list[str] = []

    def add(self, sensor: Sensor) -> Sensor:
        self.sensors[sensor.id] = sensor
        return sensor

    def list_all(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        sensors = list(self.sensors.values())
        return sensors[offset : offset + limit]

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        self.get_arguments.append(sensor_id)
        return self.sensors.get(sensor_id)

    def update(self, sensor: Sensor) -> Sensor:
        self.sensors[sensor.id] = sensor
        return sensor


TestContext = tuple[
    ReadingService,
    FakeReadingRepository,
    FakeSensorRepository,
]


def fixed_clock() -> datetime:
    """Devuelve una fecha fija para obtener pruebas deterministas."""

    return FIXED_TIME


@pytest.fixture
def context() -> TestContext:
    reading_repository = FakeReadingRepository()
    sensor_repository = FakeSensorRepository()

    sensor_repository.add(
        Sensor(
            id="TEMP-01",
            name="Sensor de temperatura",
            sensor_type="temperature",
            unit="C",
            is_active=True,
        )
    )
    sensor_repository.add(
        Sensor(
            id="HUM-01",
            name="Sensor de humedad",
            sensor_type="humidity",
            unit="%",
            is_active=True,
        )
    )

    service = ReadingService(
        reading_repository=reading_repository,
        sensor_repository=sensor_repository,
        clock=fixed_clock,
    )

    return service, reading_repository, sensor_repository


def create_temperature_reading(
    service: ReadingService,
) -> Reading:
    """Registra una lectura válida de temperatura."""

    return service.create_reading(
        sensor_id="TEMP-01",
        value=24.5,
        unit=SensorUnit.CELSIUS,
    )


@pytest.mark.parametrize(
    ("sensor_id", "value", "unit", "expected_unit"),
    [
        (
            "TEMP-01",
            24.5,
            SensorUnit.CELSIUS,
            "C",
        ),
        (
            "HUM-01",
            60.0,
            SensorUnit.PERCENT,
            "%",
        ),
    ],
)
def test_create_reading_stores_valid_measurement(
    context: TestContext,
    sensor_id: str,
    value: float,
    unit: SensorUnit,
    expected_unit: str,
) -> None:
    service, repository, sensor_repository = context

    reading = service.create_reading(
        sensor_id=f" {sensor_id} ",
        value=value,
        unit=unit,
    )

    assert reading.id == 1
    assert reading.sensor_id == sensor_id
    assert reading.value == value
    assert reading.unit == expected_unit
    assert reading.received_at == FIXED_TIME

    assert repository.add_calls == [reading]
    assert sensor_repository.get_arguments[-1] == sensor_id


@pytest.mark.parametrize(
    ("sensor_id", "value", "unit", "message"),
    [
        (
            "TEMP-01",
            -273.16,
            SensorUnit.CELSIUS,
            "temperatura no puede ser menor",
        ),
        (
            "TEMP-01",
            25.0,
            SensorUnit.PERCENT,
            "unidad % no corresponde",
        ),
        (
            "HUM-01",
            -0.1,
            SensorUnit.PERCENT,
            "humedad debe estar entre 0 y 100",
        ),
        (
            "HUM-01",
            100.1,
            SensorUnit.PERCENT,
            "humedad debe estar entre 0 y 100",
        ),
    ],
)
def test_create_reading_rejects_invalid_measurement(
    context: TestContext,
    sensor_id: str,
    value: float,
    unit: SensorUnit,
    message: str,
) -> None:
    service, repository, _ = context

    with pytest.raises(ValueError, match=message):
        service.create_reading(
            sensor_id=sensor_id,
            value=value,
            unit=unit,
        )

    assert repository.add_calls == []


def test_create_reading_rejects_unknown_sensor(
    context: TestContext,
) -> None:
    service, repository, sensor_repository = context

    with pytest.raises(
        LookupError,
        match="No existe el sensor",
    ):
        service.create_reading(
            sensor_id="NO-EXISTE",
            value=25.0,
            unit=SensorUnit.CELSIUS,
        )

    assert repository.add_calls == []
    assert sensor_repository.get_arguments[-1] == "NO-EXISTE"


def test_create_reading_rejects_inactive_sensor(
    context: TestContext,
) -> None:
    service, repository, sensor_repository = context
    sensor = sensor_repository.get_by_id("TEMP-01")

    assert sensor is not None

    sensor.is_active = False

    with pytest.raises(
        ValueError,
        match="está desactivado",
    ):
        service.create_reading(
            sensor_id="TEMP-01",
            value=25.0,
            unit=SensorUnit.CELSIUS,
        )

    assert repository.add_calls == []


def test_list_by_sensor_delegates_filters_and_pagination(
    context: TestContext,
) -> None:
    service, repository, sensor_repository = context

    first = Reading(
        sensor_id="TEMP-01",
        value=22.0,
        unit="C",
        received_at=RANGE_START,
    )
    first.id = 10

    second = Reading(
        sensor_id="TEMP-01",
        value=23.0,
        unit="C",
        received_at=RANGE_END,
    )
    second.id = 11

    repository.list_result = [first, second]

    result = service.list_by_sensor(
        " TEMP-01 ",
        limit=2,
        offset=1,
        from_date=RANGE_START,
        to_date=RANGE_END,
    )

    assert result == [first, second]
    assert repository.list_arguments == (
        "TEMP-01",
        2,
        1,
        RANGE_START,
        RANGE_END,
    )
    assert sensor_repository.get_arguments[-1] == "TEMP-01"


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
    service, repository, _ = context

    with pytest.raises(ValueError, match=message):
        service.list_by_sensor(
            "TEMP-01",
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    assert repository.list_arguments is None


def test_get_by_id_handles_existing_and_missing(
    context: TestContext,
) -> None:
    service, repository, _ = context
    reading = create_temperature_reading(service)

    existing = service.get_by_id(reading.id)
    missing = service.get_by_id(999)

    assert existing is reading
    assert missing is None
    assert repository.get_arguments[-2:] == [
        reading.id,
        999,
    ]


def test_update_reading_changes_value_and_persists(
    context: TestContext,
) -> None:
    service, repository, _ = context
    reading = create_temperature_reading(service)

    result = service.update_reading(
        reading.id,
        value=26.0,
    )

    assert result is reading
    assert reading.value == 26.0
    assert reading.unit == "C"
    assert repository.update_calls == [reading]


@pytest.mark.parametrize(
    ("sensor_id", "initial_value", "initial_unit", "value", "unit", "message"),
    [
        (
            "TEMP-01",
            24.5,
            SensorUnit.CELSIUS,
            None,
            SensorUnit.PERCENT,
            "unidad % no corresponde",
        ),
        (
            "TEMP-01",
            24.5,
            SensorUnit.CELSIUS,
            -273.16,
            None,
            "temperatura no puede ser menor",
        ),
        (
            "HUM-01",
            60.0,
            SensorUnit.PERCENT,
            100.1,
            None,
            "humedad debe estar entre 0 y 100",
        ),
    ],
)
def test_update_reading_rejects_invalid_measurement(
    context: TestContext,
    sensor_id: str,
    initial_value: float,
    initial_unit: SensorUnit,
    value: float | None,
    unit: SensorUnit | None,
    message: str,
) -> None:
    service, repository, _ = context

    reading = service.create_reading(
        sensor_id=sensor_id,
        value=initial_value,
        unit=initial_unit,
    )

    with pytest.raises(ValueError, match=message):
        service.update_reading(
            reading.id,
            value=value,
            unit=unit,
        )

    assert repository.update_calls == []


def test_update_reading_handles_missing(
    context: TestContext,
) -> None:
    service, repository, _ = context

    result = service.update_reading(
        999,
        value=25.0,
    )

    assert result is None
    assert repository.update_calls == []


def test_update_reading_rejects_empty_update(
    context: TestContext,
) -> None:
    service, repository, _ = context

    with pytest.raises(
        ValueError,
        match="debe proporcionar al menos un valor",
    ):
        service.update_reading(1)

    assert repository.update_calls == []


def test_delete_reading_persists_deletion(
    context: TestContext,
) -> None:
    service, repository, _ = context
    reading = create_temperature_reading(service)

    result = service.delete_reading(reading.id)

    assert result is True
    assert repository.delete_calls == [reading]
    assert repository.readings == []


def test_delete_reading_handles_missing(
    context: TestContext,
) -> None:
    service, repository, _ = context

    result = service.delete_reading(999)

    assert result is False
    assert repository.delete_calls == []