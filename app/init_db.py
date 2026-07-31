from app.db import Base, engine
from app.models import Reading, Sensor


def init_db() -> None:
    """Crea las tablas correspondientes a los modelos registrados."""

    _ = (
        Reading,
        Sensor,
    )

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()