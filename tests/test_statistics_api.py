from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_reading_service
from app.main import app

RANGE_START = datetime(2026, 8, 1, tzinfo=timezone.utc)
RANGE_END = datetime(2026, 8, 2, tzinfo=timezone.utc)


@dataclass(frozen=True)
class StatisticsResult:
    sensor_id: str
    minimum: float
    maximum: float
    average: float


class FakeStatisticsService:
    """Servicio controlado para probar el endpoint de estadísticas."""

    def __init__(self) -> None:
        self.arguments: tuple[str, datetime, datetime] | None = None
        self.result = StatisticsResult(
            sensor_id="TEMP-01",
            minimum=20.0,
            maximum=30.0,
            average=25.0,
        )
        self.error: LookupError | ValueError | None = None

    def get_statistics(
        self,
        sensor_id: str,
        *,
        from_date: datetime,
        to_date: datetime,
    ) -> StatisticsResult:
        self.arguments = (sensor_id, from_date, to_date)

        if self.error is not None:
            raise self.error

        return self.result


@contextmanager
def statistics_client(
    service: FakeStatisticsService,
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_reading_service] = lambda: service

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_reading_service, None)


def request_statistics(
    client: TestClient,
    sensor_id: str = "TEMP-01",
) -> object:
    return client.get(
        f"/sensors/{sensor_id}/statistics",
        params={
            "from": RANGE_START.isoformat(),
            "to": RANGE_END.isoformat(),
        },
    )


def test_get_statistics_returns_exact_response() -> None:
    service = FakeStatisticsService()

    with statistics_client(service) as client:
        response = request_statistics(client)

    assert response.status_code == 200
    assert response.json() == {
        "sensor_id": "TEMP-01",
        "minimum": 20.0,
        "maximum": 30.0,
        "average": 25.0,
    }
    assert service.arguments == (
        "TEMP-01",
        RANGE_START,
        RANGE_END,
    )


def test_get_statistics_returns_404_for_unknown_sensor() -> None:
    service = FakeStatisticsService()
    service.error = LookupError("No existe el sensor con id NO-EXISTE")

    with statistics_client(service) as client:
        response = request_statistics(client, "NO-EXISTE")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No existe el sensor con id NO-EXISTE"
    }


def test_get_statistics_returns_404_for_period_without_data() -> None:
    service = FakeStatisticsService()
    service.error = LookupError(
        "No existen lecturas para el sensor TEMP-01 "
        "en el período solicitado"
    )

    with statistics_client(service) as client:
        response = request_statistics(client)

    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            "No existen lecturas para el sensor TEMP-01 "
            "en el período solicitado"
        )
    }


def test_get_statistics_returns_400_for_invalid_date_range() -> None:
    service = FakeStatisticsService()
    service.error = ValueError(
        "from_date no puede ser posterior a to_date"
    )

    with statistics_client(service) as client:
        response = client.get(
            "/sensors/TEMP-01/statistics",
            params={
                "from": RANGE_END.isoformat(),
                "to": RANGE_START.isoformat(),
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "from_date no puede ser posterior a to_date"
    }


def test_get_statistics_returns_400_for_mixed_datetime_awareness() -> None:
    service = FakeStatisticsService()
    service.error = ValueError(
        "from_date y to_date deben tener la misma "
        "conciencia de zona horaria"
    )

    with statistics_client(service) as client:
        response = client.get(
            "/sensors/TEMP-01/statistics",
            params={
                "from": "2026-08-01T00:00:00",
                "to": RANGE_END.isoformat(),
            },
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "from_date y to_date deben tener la misma "
            "conciencia de zona horaria"
        )
    }


@pytest.mark.parametrize("missing_parameter", ["from", "to"])
def test_get_statistics_requires_temporal_parameters(
    missing_parameter: str,
) -> None:
    service = FakeStatisticsService()
    params = {
        "from": RANGE_START.isoformat(),
        "to": RANGE_END.isoformat(),
    }
    params.pop(missing_parameter)

    with statistics_client(service) as client:
        response = client.get(
            "/sensors/TEMP-01/statistics",
            params=params,
        )

    assert response.status_code == 422
    assert service.arguments is None
