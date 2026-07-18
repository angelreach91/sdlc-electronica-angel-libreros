import json
from io import StringIO
from logging import INFO, Logger, StreamHandler
from typing import cast

import pytest

from semana1.uart_driver.config import Parity, StopBits, UartConfig
from semana1.uart_driver.device import UartDevice
from semana1.uart_driver.json_logging import JsonFormatter
from semana1.uart_driver.parsers import MessageParser, ParsedMessage


def _valid_config() -> UartConfig:
    return UartConfig(
        baudrate=9600,
        parity=Parity.NONE,
        stop_bits=StopBits.ONE,
        timeout=1.0,
    )


class StubParser(MessageParser):
    def __init__(self, recognizes_frame: bool) -> None:
        self.recognizes_frame = recognizes_frame

    def can_parse(self, frame: bytes) -> bool:
        return self.recognizes_frame

    def parse(self, frame: bytes) -> ParsedMessage:
        return {"frame": frame.hex()}


def _build_logger(stream: StringIO) -> Logger:
    logger = Logger("uart.device.test")
    logger.setLevel(INFO)

    handler = StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger


def _read_events(stream: StringIO) -> list[dict[str, object]]:
    return [
        cast(dict[str, object], json.loads(line))
        for line in stream.getvalue().splitlines()
    ]


def test_device_logs_connection_and_disconnection() -> None:
    """Debe registrar eventos al conectarse y desconectarse."""
    stream = StringIO()
    logger = _build_logger(stream)
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        logger=logger,
    )

    device.connect()
    device.disconnect()

    events = _read_events(stream)

    assert len(events) == 2
    assert [event["event"] for event in events] == [
        "uart.connected",
        "uart.disconnected",
    ]
    assert [event["level"] for event in events] == [
        "INFO",
        "INFO",
    ]


def test_device_logs_successfully_parsed_frame() -> None:
    """Debe registrar un evento después de procesar una trama."""
    stream = StringIO()
    logger = _build_logger(stream)
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        logger=logger,
    )

    device.connect()
    device.read_and_parse(b"first frame")

    events = _read_events(stream)

    assert [event["event"] for event in events] == [
        "uart.connected",
        "uart.frame_parsed",
    ]
    assert events[1]["level"] == "INFO"
    assert "first frame" not in stream.getvalue()


def test_device_logs_disconnected_read_rejection() -> None:
    """Debe registrar una advertencia al intentar leer desconectado."""
    stream = StringIO()
    logger = _build_logger(stream)
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        logger=logger,
    )

    with pytest.raises(RuntimeError, match=r"(?i)conect"):
        device.read_and_parse(b"first frame")

    events = _read_events(stream)

    assert len(events) == 1
    assert events[0]["event"] == "uart.read_rejected"
    assert events[0]["level"] == "WARNING"


def test_device_logs_unrecognized_frame() -> None:
    """Debe registrar una advertencia cuando el parser rechaza la trama."""
    stream = StringIO()
    logger = _build_logger(stream)
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=False),
        logger=logger,
    )

    device.connect()

    with pytest.raises(ValueError, match=r"(?i)reconoc"):
        device.read_and_parse(b"first frame")

    events = _read_events(stream)

    assert [event["event"] for event in events] == [
        "uart.connected",
        "uart.frame_unrecognized",
    ]
    assert events[1]["level"] == "WARNING"
    assert all(
        event["event"] != "uart.frame_parsed"
        for event in events
    )