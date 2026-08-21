import io
import json
import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_app_config
from app.dependencies import get_sensor_service
from app.exceptions import SensorAlreadyExistsError
from app.main import app
from app.observability import JsonFormatter, MetricsCollector


class FailingSensorService:
    """Servicio controlado que propaga el error indicado."""

    def __init__(self, error: Exception) -> None:
        self.error = error

    def create_sensor(self, **_: object) -> None:
        raise self.error


def _post_sensor_with_error(error: Exception) -> tuple[int, dict[str, str]]:
    app.dependency_overrides[get_sensor_service] = lambda: FailingSensorService(
        error
    )

    try:
        with TestClient(
            app,
            raise_server_exceptions=False,
        ) as client:
            response = client.post(
                "/sensors",
                json={
                    "id": "TEMP-01",
                    "name": "Sensor exterior",
                    "sensor_type": "temperature",
                    "unit": "C",
                    "location": "Exterior",
                },
            )
    finally:
        app.dependency_overrides.pop(get_sensor_service, None)

    return response.status_code, response.json()


def test_metrics_endpoint_returns_only_basic_metrics() -> None:
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert set(response.json()) == {
        "requests_total",
        "errors_total",
        "uptime_seconds",
    }
    assert isinstance(response.json()["requests_total"], int)
    assert isinstance(response.json()["errors_total"], int)
    assert isinstance(response.json()["uptime_seconds"], int | float)
    assert response.json()["uptime_seconds"] >= 0


def test_metrics_collector_counts_requests_and_errors() -> None:
    collector = MetricsCollector()

    initial = collector.snapshot()
    collector.record_request(200)
    collector.record_request(399)
    collector.record_request(400)
    collector.record_request(503)
    current = collector.snapshot()

    assert initial["requests_total"] == 0
    assert initial["errors_total"] == 0
    assert initial["uptime_seconds"] >= 0
    assert current["requests_total"] == 4
    assert current["errors_total"] == 2
    assert current["uptime_seconds"] >= 0


def test_json_formatter_emits_valid_structured_log() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="sensorhub.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="http_request",
        args=(),
        exc_info=None,
    )
    record.event_fields = {
        "method": "GET",
        "path": "/health",
        "status_code": 200,
        "duration_ms": 1.25,
    }

    payload = json.loads(formatter.format(record))

    assert payload == {
        "event": "http_request",
        "method": "GET",
        "path": "/health",
        "status_code": 200,
        "duration_ms": 1.25,
    }


def test_app_config_reads_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_NAME", "SensorHub Test")
    monkeypatch.setenv("APP_VERSION", "9.8.7")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    config = get_app_config()

    assert config.app_name == "SensorHub Test"
    assert config.app_version == "9.8.7"
    assert config.log_level == "DEBUG"


@pytest.mark.parametrize(
    ("error", "expected_status"),
    [
        (ValueError("solicitud inválida"), 400),
        (LookupError("recurso inexistente"), 404),
        (SensorAlreadyExistsError("sensor duplicado"), 409),
    ],
)
def test_known_errors_use_global_handlers(
    error: Exception,
    expected_status: int,
) -> None:
    status_code, payload = _post_sensor_with_error(error)

    assert status_code == expected_status
    assert payload == {"detail": str(error)}


def test_persistence_error_returns_safe_503() -> None:
    status_code, payload = _post_sensor_with_error(
        SQLAlchemyError("postgresql://secret@db")
    )

    assert status_code == 503
    assert payload == {"detail": "Error de persistencia"}


def test_unexpected_error_returns_safe_500() -> None:
    status_code, payload = _post_sensor_with_error(
        RuntimeError("dato interno sensible")
    )

    assert status_code == 500
    assert payload == {"detail": "Error interno del servidor"}


def test_controlled_error_emits_structured_application_log() -> None:
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("sensorhub")
    logger.addHandler(handler)

    try:
        _post_sensor_with_error(ValueError("solicitud inválida"))
    finally:
        logger.removeHandler(handler)

    events = [json.loads(line) for line in stream.getvalue().splitlines()]
    error_event = next(
        event for event in events if event["event"] == "application_error"
    )

    assert error_event["error_type"] == "ValueError"
    assert error_event["path"] == "/sensors"
    assert error_event["detail"] == "solicitud inválida"
