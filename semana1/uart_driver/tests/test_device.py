import pytest

from semana1.uart_driver.config import Parity, StopBits, UartConfig
from semana1.uart_driver.device import UartDevice
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
        self.last_frame: bytes | None = None
        self.can_parse_calls = 0
        self.parse_calls = 0

    def can_parse(self, frame: bytes) -> bool:
        self.last_frame = frame
        self.can_parse_calls += 1
        return self.recognizes_frame

    def parse(self, frame: bytes) -> ParsedMessage:
        self.last_frame = frame
        self.parse_calls += 1
        return {"frame": frame.hex()}


def test_device_starts_disconnected_with_injected_config() -> None:
    """Debe iniciar desconectado y conservar la configuración inyectada."""
    config = _valid_config()
    device = UartDevice(config, StubParser(recognizes_frame=True))

    assert device.is_connected is False
    assert device.config is config


def test_device_connects_and_uses_injected_parser() -> None:
    """Debe procesar una trama mediante el parser inyectado al conectarse."""
    parser = StubParser(recognizes_frame=True)
    device = UartDevice(_valid_config(), parser)
    frame = b"example frame"

    device.connect()
    result = device.read_and_parse(frame)

    assert device.is_connected is True
    assert result == {"frame": frame.hex()}
    assert parser.can_parse_calls == 1
    assert parser.parse_calls == 1
    assert parser.last_frame == frame


def test_device_rejects_read_when_disconnected() -> None:
    """Debe rechazar una lectura cuando el dispositivo no está conectado."""
    parser = StubParser(recognizes_frame=True)
    device = UartDevice(_valid_config(), parser)

    with pytest.raises(RuntimeError, match=r"(?i)conect"):
        device.read_and_parse(b"example frame")

    assert parser.can_parse_calls == 0
    assert parser.parse_calls == 0


def test_device_rejects_unsupported_frame() -> None:
    """Debe rechazar una trama que el parser inyectado no reconoce."""
    parser = StubParser(recognizes_frame=False)
    device = UartDevice(_valid_config(), parser)
    frame = b"unsupported frame"
    device.connect()

    with pytest.raises(ValueError, match=r"(?i)reconoc"):
        device.read_and_parse(frame)

    assert parser.can_parse_calls == 1
    assert parser.parse_calls == 0
    assert parser.last_frame == frame


def test_devices_keep_independent_connection_states() -> None:
    """Dos dispositivos deben conservar estados de conexión independientes."""
    first_device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
    )
    second_device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
    )

    first_device.connect()

    assert first_device.is_connected is True
    assert second_device.is_connected is False

    second_device.connect()
    first_device.disconnect()

    assert first_device.is_connected is False
    assert second_device.is_connected is True


def test_device_disconnects_and_rejects_new_reads() -> None:
    """Debe impedir nuevas lecturas después de desconectarse."""
    parser = StubParser(recognizes_frame=True)
    device = UartDevice(_valid_config(), parser)
    device.connect()

    device.disconnect()

    assert device.is_connected is False

    with pytest.raises(RuntimeError, match=r"(?i)conect"):
        device.read_and_parse(b"example frame")

    assert parser.can_parse_calls == 0
    assert parser.parse_calls == 0