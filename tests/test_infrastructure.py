import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import get_app_config
from app.db import get_database_url
from app.dependencies import get_session
from app.main import app

client = TestClient(app)


def test_normalizes_postgres_database_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Normaliza la URL corta entregada por algunos proveedores."""

    monkeypatch.setenv(
        "DATABASE_URL",
        "postgres://sensor:secret@db:5432/sensorhub",
    )

    assert get_database_url() == (
        "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    )


def test_normalizes_postgresql_database_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Agrega explícitamente el controlador psycopg."""

    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://sensor:secret@db:5432/sensorhub",
    )

    assert get_database_url() == (
        "postgresql+psycopg://sensor:secret@db:5432/sensorhub"
    )


def test_get_session_provides_sqlalchemy_session() -> None:
    """Comprueba la dependencia que entrega sesiones de SQLAlchemy."""

    session_generator = get_session()
    session = next(session_generator)

    assert isinstance(session, Session)

    session_generator.close()


def test_health_endpoint() -> None:
    """Comprueba que el endpoint de salud responde correctamente."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_config_uses_safe_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proporciona valores no sensibles cuando no existe configuración."""

    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    config = get_app_config()

    assert config.app_name == "SensorHub"
    assert config.app_version == "0.6.0"
    assert config.log_level == "INFO"
