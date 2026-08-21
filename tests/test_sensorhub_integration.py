from collections.abc import Generator
from datetime import datetime, timedelta
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
            "location": "Exterior",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201
    assert sensor_response.json() == {
        "id": "TEMP-01",
        "name": "Sensor exterior",
        "location": "Exterior",
        "sensor_type": "temperature",
        "unit": "C",
        "is_active": True,
        "threshold": None,
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


def test_list_readings_applies_pagination_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba la paginación contra la persistencia real."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-PAGE",
            "name": "Sensor de paginación",
            "location": "Laboratorio",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    reading_responses = [
        client.post(
            "/sensors/TEMP-PAGE/readings",
            json={
                "value": value,
                "unit": "C",
            },
        )
        for value in (21.0, 22.0, 23.0)
    ]

    assert all(
        response.status_code == 201
        for response in reading_responses
    )

    second_reading = reading_responses[1].json()
    list_response = client.get(
        "/sensors/TEMP-PAGE/readings",
        params={
            "limit": 1,
            "offset": 1,
        },
    )

    assert list_response.status_code == 200
    assert list_response.json() == [second_reading]
    assert list_response.json()[0]["sensor_id"] == "TEMP-PAGE"


def test_list_readings_applies_to_filter_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba que el filtro final excluye lecturas posteriores."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-TIME",
            "name": "Sensor temporal",
            "location": "Laboratorio",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    reading_response = client.post(
        "/sensors/TEMP-TIME/readings",
        json={
            "value": 24.5,
            "unit": "C",
        },
    )

    assert reading_response.status_code == 201

    received_at = datetime.fromisoformat(
        reading_response.json()["received_at"]
    )
    immediately_before = received_at - timedelta(microseconds=1)

    list_response = client.get(
        "/sensors/TEMP-TIME/readings",
        params={
            "to": immediately_before.isoformat(),
        },
    )

    assert list_response.status_code == 200
    assert list_response.json() == []


def test_list_readings_rejects_invalid_date_range_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba el error controlado para un rango temporal inválido."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-RANGE",
            "name": "Sensor de rango",
            "location": "Laboratorio",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    list_response = client.get(
        "/sensors/TEMP-RANGE/readings",
        params={
            "from": "2026-08-21T12:00:00+00:00",
            "to": "2026-08-21T11:59:59+00:00",
        },
    )

    assert list_response.status_code == 400
    assert list_response.json() == {
        "detail": "from_date no puede ser posterior a to_date"
    }


def test_update_delete_and_deactivate_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba actualización, eliminación y desactivación."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-01",
            "name": "Sensor exterior",
            "location": "Exterior",
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


def test_configure_threshold_detect_and_query_alert_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba el flujo completo de detección y consulta de alertas."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-01",
            "name": "Sensor exterior",
            "location": "Exterior",
            "sensor_type": "temperature",
            "unit": "C",
        },
    )

    assert sensor_response.status_code == 201

    threshold_response = client.patch(
        "/sensors/TEMP-01",
        json={
            "threshold": 30.0,
        },
    )

    assert threshold_response.status_code == 200
    assert threshold_response.json()["threshold"] == 30.0

    reading_response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "value": 31.5,
            "unit": "C",
        },
    )

    assert reading_response.status_code == 201

    reading_id = reading_response.json()["id"]
    alerts_response = client.get("/sensors/TEMP-01/alerts")

    assert alerts_response.status_code == 200

    alerts = alerts_response.json()

    assert len(alerts) == 1
    assert alerts[0]["sensor_id"] == "TEMP-01"
    assert alerts[0]["reading_id"] == reading_id
    assert alerts[0]["value"] == 31.5
    assert alerts[0]["threshold"] == 30.0
    assert alerts[0]["id"] is not None
    assert alerts[0]["created_at"] is not None

    equal_reading_response = client.post(
        "/sensors/TEMP-01/readings",
        json={
            "value": 30.0,
            "unit": "C",
        },
    )

    assert equal_reading_response.status_code == 201

    alerts_after_equal_reading = client.get(
        "/sensors/TEMP-01/alerts"
    )

    assert alerts_after_equal_reading.status_code == 200
    assert alerts_after_equal_reading.json() == alerts


def test_alert_lifecycle_updates_active_alerts_with_sqlite(
    client: TestClient,
) -> None:
    """Comprueba el ciclo completo de una alerta hasta su resolución."""

    sensor_response = client.post(
        "/sensors",
        json={
            "id": "TEMP-LIFECYCLE",
            "name": "Sensor de ciclo de alerta",
            "location": "Laboratorio",
            "sensor_type": "temperature",
            "unit": "C",
            "threshold": 30.0,
        },
    )
    assert sensor_response.status_code == 201

    reading_response = client.post(
        "/sensors/TEMP-LIFECYCLE/readings",
        json={"value": 31.5, "unit": "C"},
    )
    assert reading_response.status_code == 201

    alerts_response = client.get(
        "/sensors/TEMP-LIFECYCLE/alerts"
    )
    assert alerts_response.status_code == 200
    alert = alerts_response.json()[0]
    alert_id = alert["id"]
    assert alert["status"] == "open"

    acknowledge_response = client.patch(
        f"/alerts/{alert_id}/status",
        json={"status": "acknowledged"},
    )
    assert acknowledge_response.status_code == 200
    assert acknowledge_response.json()["status"] == "acknowledged"

    active_response = client.get("/alerts/active")
    assert active_response.status_code == 200
    assert alert_id in [item["id"] for item in active_response.json()]

    resolve_response = client.patch(
        f"/alerts/{alert_id}/status",
        json={"status": "resolved"},
    )
    assert resolve_response.status_code == 200
    assert resolve_response.json()["status"] == "resolved"

    active_after_resolution = client.get("/alerts/active")
    assert active_after_resolution.status_code == 200
    assert alert_id not in [
        item["id"] for item in active_after_resolution.json()
    ]
