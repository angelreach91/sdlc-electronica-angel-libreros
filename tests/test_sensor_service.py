import pytest

from app.exceptions import SensorAlreadyExistsError
from app.models.sensor import Sensor
from app.sensor_types import SensorType, SensorUnit
from app.services.sensor_service import SensorService


class FakeSensorRepository:
    """Repositorio controlado utilizado para probar SensorService."""

    def __init__(self) -> None:
        self.sensors: dict[str, Sensor] = {}
        self.list_arguments: tuple[int, int] | None = None
        self.list_result: list[Sensor] | None = None
        self.get_arguments: list[str] = []
        self.update_calls: list[Sensor] = []

    def add(self, sensor: Sensor) -> Sensor:
        self.sensors[sensor.id] = sensor
        return sensor

    def list_all(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        self.list_arguments = (limit, offset)

        if self.list_result is not None:
            return self.list_result

        ordered = sorted(
            self.sensors.values(),
            key=lambda sensor: sensor.id,
        )
        return ordered[offset : offset + limit]

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        self.get_arguments.append(sensor_id)
        return self.sensors.get(sensor_id)

    def update(self, sensor: Sensor) -> Sensor:
        self.update_calls.append(sensor)
        self.sensors[sensor.id] = sensor
        return sensor


TestContext = tuple[SensorService, FakeSensorRepository]


@pytest.fixture
def context() -> TestContext:
    repository = FakeSensorRepository()
    return SensorService(repository), repository


def create_temperature_sensor(service: SensorService) -> Sensor:
    return service.create_sensor(
        sensor_id="TEMP-01",
        name="Sensor de temperatura",
        sensor_type=SensorType.TEMPERATURE,
        unit=SensorUnit.CELSIUS,
    )


def test_create_sensor_stores_normalized_data(
    context: TestContext,
) -> None:
    service, repository = context

    sensor = service.create_sensor(
        sensor_id=" TEMP-01 ",
        name=" Sensor exterior ",
        sensor_type=SensorType.TEMPERATURE,
        unit=SensorUnit.CELSIUS,
    )

    assert sensor.id == "TEMP-01"
    assert sensor.name == "Sensor exterior"
    assert sensor.sensor_type == "temperature"
    assert sensor.unit == "C"
    assert sensor.is_active is True
    assert repository.sensors == {"TEMP-01": sensor}


def test_create_sensor_has_no_threshold_by_default(
    context: TestContext,
) -> None:
    service, _ = context

    sensor = create_temperature_sensor(service)

    assert sensor.threshold is None


def test_create_sensor_rejects_duplicate_id(
    context: TestContext,
) -> None:
    service, _ = context
    create_temperature_sensor(service)

    with pytest.raises(
        SensorAlreadyExistsError,
        match="ya existe un sensor",
    ):
        create_temperature_sensor(service)


@pytest.mark.parametrize(
    ("sensor_type", "unit"),
    [
        (SensorType.TEMPERATURE, SensorUnit.PERCENT),
        (SensorType.HUMIDITY, SensorUnit.CELSIUS),
    ],
)
def test_create_sensor_rejects_incompatible_unit(
    context: TestContext,
    sensor_type: SensorType,
    unit: SensorUnit,
) -> None:
    service, repository = context

    with pytest.raises(
        ValueError,
        match="no corresponde",
    ):
        service.create_sensor(
            sensor_id="SENSOR-01",
            name="Sensor inválido",
            sensor_type=sensor_type,
            unit=unit,
        )

    assert repository.sensors == {}


def test_list_sensors_delegates_pagination(
    context: TestContext,
) -> None:
    service, repository = context

    first = Sensor(
        id="HUM-01",
        name="Sensor de humedad",
        sensor_type="humidity",
        unit="%",
        is_active=True,
    )
    second = Sensor(
        id="TEMP-01",
        name="Sensor de temperatura",
        sensor_type="temperature",
        unit="C",
        is_active=True,
    )

    repository.list_result = [first, second]

    result = service.list_sensors(
        limit=2,
        offset=1,
    )

    assert result == [first, second]
    assert repository.list_arguments == (2, 1)


def test_get_sensor_normalizes_id_and_handles_missing(
    context: TestContext,
) -> None:
    service, repository = context
    sensor = create_temperature_sensor(service)

    existing = service.get_by_id(" TEMP-01 ")
    missing = service.get_by_id("NO-EXISTE")

    assert existing is sensor
    assert missing is None
    assert repository.get_arguments[-2:] == [
        "TEMP-01",
        "NO-EXISTE",
    ]


def test_update_sensor_changes_fields_and_persists(
    context: TestContext,
) -> None:
    service, repository = context
    sensor = create_temperature_sensor(service)

    updated = service.update_sensor(
        sensor.id,
        name="Sensor interior",
        is_active=False,
    )

    assert updated is sensor
    assert sensor.name == "Sensor interior"
    assert sensor.sensor_type == "temperature"
    assert sensor.unit == "C"
    assert sensor.is_active is False
    assert repository.update_calls == [sensor]


def test_update_sensor_changes_only_threshold_and_persists(
    context: TestContext,
) -> None:
    service, repository = context
    sensor = create_temperature_sensor(service)
    original_name = sensor.name
    original_is_active = sensor.is_active

    updated = service.update_sensor(
        sensor.id,
        threshold=30.5,
    )

    assert updated is sensor
    assert sensor.threshold == 30.5
    assert sensor.name == original_name
    assert sensor.is_active is original_is_active
    assert repository.update_calls == [sensor]


def test_update_sensor_rejects_empty_update(
    context: TestContext,
) -> None:
    service, repository = context
    create_temperature_sensor(service)

    with pytest.raises(
        ValueError,
        match="debe proporcionar al menos un valor",
    ):
        service.update_sensor("TEMP-01")

    assert repository.update_calls == []


def test_deactivate_sensor_persists_change(
    context: TestContext,
) -> None:
    service, repository = context
    sensor = create_temperature_sensor(service)

    result = service.deactivate_sensor(sensor.id)

    assert result is True
    assert sensor.is_active is False
    assert repository.update_calls == [sensor]


def test_deactivate_sensor_handles_missing(
    context: TestContext,
) -> None:
    service, repository = context

    result = service.deactivate_sensor("NO-EXISTE")

    assert result is False
    assert repository.update_calls == []


@pytest.mark.parametrize(
    ("limit", "offset", "message"),
    [
        (0, 0, "limit debe estar entre 1 y 100"),
        (101, 0, "limit debe estar entre 1 y 100"),
        (50, -1, "offset no puede ser negativo"),
    ],
)
def test_list_sensors_rejects_invalid_pagination(
    context: TestContext,
    limit: int,
    offset: int,
    message: str,
) -> None:
    service, repository = context

    with pytest.raises(ValueError, match=message):
        service.list_sensors(
            limit=limit,
            offset=offset,
        )

    assert repository.list_arguments is None
