import pytest

from semana1.uart_driver.buffer import ThreadSafeCircularBuffer
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

    def can_parse(self, frame: bytes) -> bool:
        return self.recognizes_frame

    def parse(self, frame: bytes) -> ParsedMessage:
        return {"frame": frame.hex()}


def test_device_stores_parsed_message_in_injected_buffer() -> None:
    """Debe almacenar en el buffer el resultado procesado correctamente."""
    buffer: ThreadSafeCircularBuffer[ParsedMessage] = (
        ThreadSafeCircularBuffer(3)
    )
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        buffer=buffer,
    )

    device.connect()
    result: ParsedMessage = device.read_and_parse(b"first frame")

    assert result == {"frame": b"first frame".hex()}
    assert buffer.snapshot() == (result,)


def test_device_does_not_store_unrecognized_frame() -> None:
    """No debe modificar el buffer cuando el parser rechaza la trama."""
    buffer: ThreadSafeCircularBuffer[ParsedMessage] = (
        ThreadSafeCircularBuffer(3)
    )
    device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=False),
        buffer=buffer,
    )
    device.connect()

    with pytest.raises(ValueError, match=r"(?i)reconoc"):
        device.read_and_parse(b"unrecognized frame")

    assert len(buffer) == 0


def test_devices_keep_independent_injected_buffers() -> None:
    """Dos dispositivos deben almacenar datos en buffers independientes."""
    first_buffer: ThreadSafeCircularBuffer[ParsedMessage] = (
        ThreadSafeCircularBuffer(3)
    )
    second_buffer: ThreadSafeCircularBuffer[ParsedMessage] = (
        ThreadSafeCircularBuffer(3)
    )
    first_device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        buffer=first_buffer,
    )
    second_device = UartDevice(
        _valid_config(),
        StubParser(recognizes_frame=True),
        buffer=second_buffer,
    )

    first_device.connect()
    second_device.connect()
    first_result: ParsedMessage = first_device.read_and_parse(b"first frame")
    second_result: ParsedMessage = second_device.read_and_parse(
        b"second frame"
    )

    assert first_buffer.snapshot() == (first_result,)
    assert second_buffer.snapshot() == (second_result,)
