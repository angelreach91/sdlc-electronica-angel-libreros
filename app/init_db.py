from app.db import engine
from app.models import Reading


def init_db() -> None:
    """Crea las tablas correspondientes a los modelos ORM registrados."""
    Reading.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()