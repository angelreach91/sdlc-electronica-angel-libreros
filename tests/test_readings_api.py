from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.dependencies import get_reading_service
from app.main import app
from app.models.reading import Reading
from app.sensor_types import SensorUnit

FIXED_TIME = datetime(
    2026,
    7,
    31,
    18,
    0,
    tzinfo=timezone.utc,
)
RANGE_START = datetime(
    2026,
    7,
    30,
    0,
    0,
    tzinfo=timezone.utc,
)
RANGE_END = datetime(
    2026,
    8,
    1,
    0,
    0,
    tzinfo=timezone.utc,
)


def make_reading(
    *,
    reading_id: int,
    sensor_id: str = "TEMP-01",
    value: float = 24.5,
    unit: str = "C",
) -> Reading:
    """Construye una lectura controlada para las pruebas HTTP."""

    reading = Reading(
        sensor_id=sensor_id,
        value=value,
        unit=unit,
        received_at=FIXED_TIME,
    )
    reading.id = reading_id

    return reading


class FakeReadingService:
    """Servicio controlado utilizado para probar el router de lecturas."""

    def __init__(self) -> None:
        self.create_arguments: (
            tuple[str, float, SensorUnit] | None
        ) = None
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
        self.update_arguments: (
            tuple[int, float | None, SensorUnit | None] | None
        ) = None

        self.create_error: ValueError | LookupError | None = None
        self.update_error: ValueError | LookupError | None = None

        self.list_result: list[Reading] = [
            make_reading(
                reading_id=2,
                value=24.5,
            ),
            make_reading(
                reading_id=3,
                value=25.0,
            ),
        ]
        self.update_result: Reading | None = make_reading(
            reading_id=7,
            value=27.5,
        )

    def create_reading(
        self,
        sensor_id: str,
        value: float,
        unit: SensorUnit,
    ) -> Reading:
        self.create_arguments = (
            sensor_id,
            value,
            unit,
        )

        if self.create_error is not None:
            raise self.create_error

        return make_reading(
            reading_id=1,
            sensor_id=sensor_id,
            value=value,
            unit=unit.value,
        )

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
        return None

    def update_reading(
        self,
        reading_id: int,
        *,
        value: float | None = None,
        unit: SensorUnit | None = None,
    ) -> Reading | None:
        self.update_arguments = (
            reading_id,
            value,
            unit,
        )

        if self.update_error is not None:
            raise self.update_error

        return self.update_result

    def delete_reading(self, reading_id: int) -> bool:
        return False


@contextmanager
def reading_client(
    service: FakeReadingService,
) -> Generator[TestClient, None, None]:
    """Proporciona un cliente con el servicio de lecturas sustituido."""

    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(
            get_reading_service,
            None,
        )


def test_create_reading_returns_created_reading() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.post(
            "/sensors/TEMP-01/readings",
            json={
                "value": 24.5,
                "unit": "C",
            },
        )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["sensor_id"] == "TEMP-01"
    assert response_data["value"] == 24.5
    assert response_data["unit"] == "C"

    received_at = datetime.fromisoformat(
        response_data["received_at"].replace(
            "Z",
            "+00:00",
        )
    )
    assert received_at == FIXED_TIME

    assert service.create_arguments == (
        "TEMP-01",
        24.5,
        SensorUnit.CELSIUS,
    )


def test_list_readings_forwards_filters_and_pagination() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.get(
            "/sensors/TEMP-01/readings",
            params={
                "limit": 2,
                "offset": 1,
                "from": RANGE_START.isoformat(),
                "to": RANGE_END.isoformat(),
            },
        )

    assert response.status_code == 200

    response_data = response.json()

    assert [reading["id"] for reading in response_data] == [
        2,
        3,
    ]
    assert [reading["value"] for reading in response_data] == [
        24.5,
        25.0,
    ]

    assert service.list_arguments == (
        "TEMP-01",
        2,
        1,
        RANGE_START,
        RANGE_END,
    )


def test_update_reading_forwards_partial_change() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.patch(
            "/readings/7",
            json={
                "value": 27.5,
            },
        )

    assert response.status_code == 200
    assert response.json()["id"] == 7
    assert response.json()["value"] == 27.5
    assert response.json()["unit"] == "C"

    assert service.update_arguments == (
        7,
        27.5,
        None,
    )


def test_update_reading_rejects_explicit_null_value() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.patch(
            "/readings/7",
            json={
                "value": None,
            },
        )

    assert response.status_code == 422
    assert service.update_arguments is None


def test_update_reading_rejects_explicit_null_unit() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.patch(
            "/readings/7",
            json={
                "unit": None,
            },
        )

    assert response.status_code == 422
    assert service.update_arguments is None


def test_create_reading_returns_404_for_unknown_sensor() -> None:
    service = FakeReadingService()
    service.create_error = LookupError(
        "No existe el sensor con id NO-EXISTE"
    )

    with reading_client(service) as client:
        response = client.post(
            "/sensors/NO-EXISTE/readings",
            json={
                "value": 24.5,
                "unit": "C",
            },
        )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No existe el sensor con id NO-EXISTE"
    }


def test_update_reading_translates_business_error_to_400() -> None:
    service = FakeReadingService()
    service.update_error = ValueError(
        "la temperatura no puede ser menor que -273.15 °C"
    )

    with reading_client(service) as client:
        response = client.patch(
            "/readings/7",
            json={
                "value": -273.16,
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "la temperatura no puede ser menor "
            "que -273.15 °C"
        )
    }


def test_create_reading_rejects_unknown_unit_with_422() -> None:
    service = FakeReadingService()

    with reading_client(service) as client:
        response = client.post(
            "/sensors/TEMP-01/readings",
            json={
                "value": 24.5,
                "unit": "fahrenheit",
            },
        )

    assert response.status_code == 422
    assert service.create_arguments is None
