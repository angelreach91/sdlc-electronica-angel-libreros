from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient

from app.dependencies import get_sensor_service
from app.exceptions import SensorAlreadyExistsError
from app.main import app
from app.models.sensor import Sensor
from app.sensor_types import SensorType, SensorUnit


class FakeSensorService:
    """Servicio controlado utilizado para probar el router de sensores."""

    def __init__(self) -> None:
        self.create_arguments: (
            tuple[str, str, SensorType, SensorUnit] | None
        ) = None
        self.list_arguments: tuple[int, int] | None = None
        self.get_arguments: str | None = None
        self.update_arguments: (
            tuple[str, str | None, bool | None] | None
        ) = None

        self.create_error: ValueError | None = None
        self.get_result: Sensor | None = Sensor(
            id="TEMP-01",
            name="Sensor de temperatura",
            sensor_type="temperature",
            unit="C",
            is_active=True,
        )

    def create_sensor(
        self,
        sensor_id: str,
        name: str,
        sensor_type: SensorType,
        unit: SensorUnit,
    ) -> Sensor:
        self.create_arguments = (
            sensor_id,
            name,
            sensor_type,
            unit,
        )

        if self.create_error is not None:
            raise self.create_error

        return Sensor(
            id=sensor_id,
            name=name,
            sensor_type=sensor_type.value,
            unit=unit.value,
            is_active=True,
        )

    def list_sensors(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Sensor]:
        self.list_arguments = (limit, offset)

        return [
            Sensor(
                id="HUM-01",
                name="Sensor de humedad",
                sensor_type="humidity",
                unit="%",
                is_active=True,
            ),
            Sensor(
                id="TEMP-01",
                name="Sensor de temperatura",
                sensor_type="temperature",
                unit="C",
                is_active=True,
            ),
        ]

    def get_by_id(self, sensor_id: str) -> Sensor | None:
        self.get_arguments = sensor_id
        return self.get_result

    def update_sensor(
        self,
        sensor_id: str,
        *,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> Sensor | None:
        self.update_arguments = (
            sensor_id,
            name,
            is_active,
        )
        return None

    def deactivate_sensor(self, sensor_id: str) -> bool:
        return False


@contextmanager
def sensor_client(
    service: FakeSensorService,
) -> Generator[TestClient, None, None]:
    """Proporciona un cliente con el servicio de sensores sustituido."""

    app.dependency_overrides[get_sensor_service] = lambda: service

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(
            get_sensor_service,
            None,
        )


def test_create_sensor_returns_created_sensor() -> None:
    service = FakeSensorService()

    with sensor_client(service) as client:
        response = client.post(
            "/sensors",
            json={
                "id": "TEMP-01",
                "name": "Sensor exterior",
                "sensor_type": "temperature",
                "unit": "C",
            },
        )

    assert response.status_code == 201
    assert response.json() == {
        "id": "TEMP-01",
        "name": "Sensor exterior",
        "sensor_type": "temperature",
        "unit": "C",
        "is_active": True,
    }

    assert service.create_arguments == (
        "TEMP-01",
        "Sensor exterior",
        SensorType.TEMPERATURE,
        SensorUnit.CELSIUS,
    )


def test_list_sensors_forwards_pagination() -> None:
    service = FakeSensorService()

    with sensor_client(service) as client:
        response = client.get(
            "/sensors",
            params={
                "limit": 2,
                "offset": 1,
            },
        )

    assert response.status_code == 200

    response_data = response.json()

    assert [sensor["id"] for sensor in response_data] == [
        "HUM-01",
        "TEMP-01",
    ]
    assert response_data[0]["unit"] == "%"
    assert response_data[1]["unit"] == "C"

    assert service.list_arguments == (2, 1)


def test_create_sensor_translates_business_error_to_400() -> None:
    service = FakeSensorService()
    service.create_error = ValueError(
        "la unidad % no corresponde al tipo temperature"
    )

    with sensor_client(service) as client:
        response = client.post(
            "/sensors",
            json={
                "id": "TEMP-01",
                "name": "Sensor exterior",
                "sensor_type": "temperature",
                "unit": "%",
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "la unidad % no corresponde "
            "al tipo temperature"
        )
    }


def test_create_sensor_translates_duplicate_to_409() -> None:
    service = FakeSensorService()
    service.create_error = SensorAlreadyExistsError(
        "ya existe un sensor con id TEMP-01"
    )

    with sensor_client(service) as client:
        response = client.post(
            "/sensors",
            json={
                "id": "TEMP-01",
                "name": "Sensor exterior",
                "sensor_type": "temperature",
                "unit": "C",
            },
        )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "ya existe un sensor con id TEMP-01"
    }


def test_get_sensor_returns_404_when_missing() -> None:
    service = FakeSensorService()
    service.get_result = None

    with sensor_client(service) as client:
        response = client.get("/sensors/NO-EXISTE")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No existe el sensor con id NO-EXISTE"
    }
    assert service.get_arguments == "NO-EXISTE"


def test_create_sensor_rejects_unknown_type_with_422() -> None:
    service = FakeSensorService()

    with sensor_client(service) as client:
        response = client.post(
            "/sensors",
            json={
                "id": "TEMP-01",
                "name": "Sensor exterior",
                "sensor_type": "thermometer",
                "unit": "C",
            },
        )

    assert response.status_code == 422
    assert service.create_arguments is None


def test_update_sensor_rejects_type_and_unit_with_422() -> None:
    service = FakeSensorService()

    with sensor_client(service) as client:
        response = client.patch(
            "/sensors/TEMP-01",
            json={
                "sensor_type": "humidity",
                "unit": "%",
            },
        )

    assert response.status_code == 422
    assert service.update_arguments is None
