import os

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)


def get_database_url() -> str:
    """Obtiene y normaliza la URL de conexión a la base de datos."""

    url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./sensorhub.db",
    )

    if url.startswith("postgres://"):
        return url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    return url


DATABASE_URL = get_database_url()

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""


SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
