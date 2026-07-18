import json
from datetime import datetime
from io import StringIO
from logging import INFO, Logger, StreamHandler
from typing import cast

from semana1.uart_driver.json_logging import JsonFormatter


def _build_logger(stream: StringIO) -> Logger:
    logger = Logger("uart.test")
    logger.setLevel(INFO)

    handler = StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger


def test_json_formatter_outputs_required_fields() -> None:
    """Debe producir JSON con timestamp, nivel, logger y evento."""
    stream = StringIO()
    logger = _build_logger(stream)

    logger.info("uart.connected")

    lines = stream.getvalue().splitlines()

    assert len(lines) == 1

    payload = cast(dict[str, object], json.loads(lines[0]))

    assert set(payload) == {
        "timestamp",
        "level",
        "logger",
        "event",
    }
    assert payload["level"] == "INFO"
    assert payload["logger"] == "uart.test"
    assert payload["event"] == "uart.connected"

    timestamp = payload["timestamp"]

    assert isinstance(timestamp, str)

    iso_timestamp = (
        timestamp[:-1] + "+00:00"
        if timestamp.endswith("Z")
        else timestamp
    )
    parsed_timestamp = datetime.fromisoformat(iso_timestamp)
    utc_offset = parsed_timestamp.utcoffset()

    assert parsed_timestamp.tzinfo is not None
    assert utc_offset is not None
    assert utc_offset.total_seconds() == 0


def test_json_formatter_preserves_unicode() -> None:
    """Debe conservar caracteres Unicode legibles en el evento."""
    stream = StringIO()
    logger = _build_logger(stream)

    logger.info("medición.recibida.México")

    lines = stream.getvalue().splitlines()

    assert len(lines) == 1

    line = lines[0]

    assert "medición.recibida.México" in line
    assert "\\u" not in line

    payload = cast(dict[str, object], json.loads(line))

    assert payload["event"] == "medición.recibida.México"


def test_json_formatter_writes_one_object_per_record() -> None:
    """Cada evento debe ocupar exactamente una línea JSON independiente."""
    stream = StringIO()
    logger = _build_logger(stream)

    logger.info("uart.connected")
    logger.info("uart.disconnected")

    lines = stream.getvalue().splitlines()

    assert len(lines) == 2

    first_payload = cast(dict[str, object], json.loads(lines[0]))
    second_payload = cast(dict[str, object], json.loads(lines[1]))

    assert [
        first_payload["event"],
        second_payload["event"],
    ] == [
        "uart.connected",
        "uart.disconnected",
    ]