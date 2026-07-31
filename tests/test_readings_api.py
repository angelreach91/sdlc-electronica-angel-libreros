from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.dependencies import get_reading_service
from app.main import app
from app.models.reading import Reading

FIXED_TIME = datetime(2026, 7, 30, 18, 0, tzinfo=timezone.utc)
SECOND_TIME = datetime(2026, 7, 30, 19, 0, tzinfo=timezone.utc)
RANGE_START = datetime(2026, 7, 29, 0, 0, tzinfo=timezone.utc)
RANGE_END = datetime(2026, 7, 31, 0, 0, tzinfo=timezone.utc)


class FakeReadingService:
    """Servicio controlado utilizado para probar únicamente la capa HTTP."""

    def __init__(self) -> None:
        self.create_arguments: tuple[str, float, float] | None = None
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
        self.get_arguments: int | None = None
        self.update_arguments: (
            tuple[int, float | None, float | None] | None
        ) = None
        self.delete_arguments: int | None = None

    def create_reading(
        self,
        sensor_id: str,
        temperature: float,
        humidity: float,
    ) -> Reading:
        self.create_arguments = (
            sensor_id,
            temperature,
            humidity,
        )

        reading = Reading(
            sensor_id=sensor_id,
            temperature=temperature,
            humidity=humidity,
            received_at=FIXED_TIME,
        )
        reading.id = 1

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

        first = Reading(
            sensor_id=sensor_id,
            temperature=24.5,
            humidity=60.0,
            received_at=FIXED_TIME,
        )
        first.id = 2

        second = Reading(
            sensor_id=sensor_id,
            temperature=25.0,
            humidity=62.0,
            received_at=SECOND_TIME,
        )
        second.id = 3

        return [first, second]

    def get_by_id(self, reading_id: int) -> Reading | None:
        self.get_arguments = reading_id

        reading = Reading(
            sensor_id="sensor-01",
            temperature=26.5,
            humidity=64.0,
            received_at=FIXED_TIME,
        )
        reading.id = reading_id

        return reading

    def update_reading(
        self,
        reading_id: int,
        *,
        temperature: float | None = None,
        humidity: float | None = None,
    ) -> Reading | None:
        self.update_arguments = (
            reading_id,
            temperature,
            humidity,
        )

        reading = Reading(
            sensor_id="sensor-01",
            temperature=26.5 if temperature is None else temperature,
            humidity=64.0 if humidity is None else humidity,
            received_at=FIXED_TIME,
        )
        reading.id = reading_id

        return reading

    def delete_reading(self, reading_id: int) -> bool:
        self.delete_arguments = reading_id
        return True


def test_create_reading_returns_created_reading() -> None:
    service = FakeReadingService()
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.post(
            "/sensors/sensor-01/readings",
            json={
                "temperature": 24.5,
                "humidity": 60.0,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["sensor_id"] == "sensor-01"
    assert response_data["temperature"] == 24.5
    assert response_data["humidity"] == 60.0

    received_at = datetime.fromisoformat(
        response_data["received_at"].replace("Z", "+00:00")
    )
    assert received_at == FIXED_TIME

    assert service.create_arguments == (
        "sensor-01",
        24.5,
        60.0,
    )


def test_list_readings_returns_filtered_page() -> None:
    service = FakeReadingService()
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get(
            "/sensors/sensor-01/readings",
            params={
                "limit": 2,
                "offset": 1,
                "from": RANGE_START.isoformat(),
                "to": RANGE_END.isoformat(),
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 2

    assert response_data[0]["id"] == 2
    assert response_data[0]["sensor_id"] == "sensor-01"
    assert response_data[0]["temperature"] == 24.5
    assert response_data[0]["humidity"] == 60.0

    assert response_data[1]["id"] == 3
    assert response_data[1]["temperature"] == 25.0
    assert response_data[1]["humidity"] == 62.0

    assert service.list_arguments == (
        "sensor-01",
        2,
        1,
        RANGE_START,
        RANGE_END,
    )


def test_get_reading_returns_existing_reading() -> None:
    service = FakeReadingService()
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.get("/readings/7")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == 7
    assert response_data["sensor_id"] == "sensor-01"
    assert response_data["temperature"] == 26.5
    assert response_data["humidity"] == 64.0

    received_at = datetime.fromisoformat(
        response_data["received_at"].replace("Z", "+00:00")
    )
    assert received_at == FIXED_TIME

    assert service.get_arguments == 7


def test_update_reading_returns_updated_reading() -> None:
    service = FakeReadingService()
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.patch(
            "/readings/7",
            json={
                "temperature": 27.5,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == 7
    assert response_data["sensor_id"] == "sensor-01"
    assert response_data["temperature"] == 27.5
    assert response_data["humidity"] == 64.0

    received_at = datetime.fromisoformat(
        response_data["received_at"].replace("Z", "+00:00")
    )
    assert received_at == FIXED_TIME

    assert service.update_arguments == (
        7,
        27.5,
        None,
    )


def test_delete_reading_returns_no_content() -> None:
    service = FakeReadingService()
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        client = TestClient(app)

        response = client.delete("/readings/7")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 204
    assert response.content == b""
    assert service.delete_arguments == 7