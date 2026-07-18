import json
from datetime import UTC, datetime
from logging import Formatter, LogRecord


class JsonFormatter(Formatter):
    """Convierte registros de logging en objetos JSON compactos."""

    def format(self, record: LogRecord) -> str:
        """Serializa un registro como una línea JSON estructurada."""
        timestamp = datetime.fromtimestamp(record.created, tz=UTC)
        timestamp_text = timestamp.isoformat(
            timespec="milliseconds"
        ).replace("+00:00", "Z")

        payload: dict[str, str] = {
            "timestamp": timestamp_text,
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }

        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )