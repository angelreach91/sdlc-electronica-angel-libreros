from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base
from app.dependencies import get_session
from app.main import app


@pytest.fixture
def client(tmp_path: Path) -> Generator[TestClient, None, None]:
    """Proporciona una API conectada a una base SQLite temporal."""

    database_path = tmp_path / "sensorhub-integration.db"

    engine = create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )

    testing_session_local: sessionmaker[Session] = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_session() -> Generator[Session, None, None]:
        with testing_session_local() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(
            get_session,
            None,
        )
        engine.dispose()


def test_create_and_query_reading_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba creación y consulta usando todas las capas reales."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-01",
            "name": "Sensor exterior",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201
    assert sensor_response.json() == {
        "id": "TEMP-01",
        "name": "Sensor exterior",
        "sensor_type": "temperature",
        "unit": "C",
        "is_active": True,
    }

    reading_response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "value": 24.5,
            "unit": "C",
        },
    )

    assert reading_response.status_code == 201

    reading_data = reading_response.json()
    reading_id = reading_data["id"]

    assert reading_data["sensor_id"] == "TEMP-01"
    assert reading_data["value"] == 24.5
    assert reading_data["unit"] == "C"

    list_response = client.get(
        "/sensors/TEMP-01/readings",
        params={
            "limit": 50,
            "offset": 0,
        },
    )

    assert list_response.status_code == 200

    listed_readings = list_response.json()

    assert len(listed_readings) == 1
    assert listed_readings[0]["id"] == reading_id
    assert listed_readings[0]["value"] == 24.5

    get_response = client.get(
        f"/readings/{reading_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == reading_id
    assert get_response.json()["sensor_id"] == "TEMP-01"
    assert get_response.json()["unit"] == "C"


def test_update_delete_and_deactivate_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba actualización, eliminación y desactivación."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-01",
            "name": "Sensor exterior",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    update_sensor_response = client.patch(
        "/sensors/TEMP-01",
        json={
            "name": "Sensor interior",
        },
    )

    assert update_sensor_response.status_code == 200
    assert update_sensor_response.json()["name"] == (
        "Sensor interior"
    )
    assert update_sensor_response.json()["is_active"] is True

    reading_response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "value": 24.5,
            "unit": "C",
        },
    )

    assert reading_response.status_code == 201

    reading_id = reading_response.json()["id"]

    update_reading_response = client.patch(
        f"/readings/{reading_id}",
        json={
            "value": 27.5,
        },
    )

    assert update_reading_response.status_code == 200
    assert update_reading_response.json()["value"] == 27.5
    assert update_reading_response.json()["unit"] == "C"

    delete_reading_response = client.delete(
        f"/readings/{reading_id}"
    )

    assert delete_reading_response.status_code == 204

    missing_reading_response = client.get(
        f"/readings/{reading_id}"
    )

    assert missing_reading_response.status_code == 404

    deactivate_sensor_response = client.delete(
        "/sensors/TEMP-01"
    )

    assert deactivate_sensor_response.status_code == 204

    sensor_after_deactivation = client.get(
        "/sensors/TEMP-01"
    )

    assert sensor_after_deactivation.status_code == 200
    assert (
        sensor_after_deactivation.json()["is_active"]
        is False
    )

    inactive_reading_response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "value": 30.0,
            "unit": "C",
        },
    )

    assert inactive_reading_response.status_code == 400