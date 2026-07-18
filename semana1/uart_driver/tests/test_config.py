from dataclasses import FrozenInstanceError

import pytest

from semana1.uart_driver.config import Parity, StopBits, UartConfig


def test_creates_valid_uart_config() -> None:
    """Debe crear una configuración cuando todos los valores son válidos."""
    config = UartConfig(
        baudrate=9600,
        parity=Parity.NONE,
        stop_bits=StopBits.ONE,
        timeout=1.0,
    )

    assert config.baudrate == 9600
    assert config.parity is Parity.NONE
    assert config.stop_bits is StopBits.ONE
    assert config.timeout == 1.0


def test_rejects_invalid_baudrate() -> None:
    """Debe rechazar un baudrate que no sea mayor que cero."""
    with pytest.raises(ValueError, match="baudrate"):
        UartConfig(
            baudrate=0,
            parity=Parity.NONE,
            stop_bits=StopBits.ONE,
            timeout=1.0,
        )


def test_uart_config_is_immutable() -> None:
    """Debe impedir que una configuración existente sea modificada."""
    config = UartConfig(
        baudrate=9600,
        parity=Parity.NONE,
        stop_bits=StopBits.ONE,
        timeout=1.0,
    )

    with pytest.raises(FrozenInstanceError):
        setattr(config, "baudrate", 115200)

def test_rejects_invalid_parity() -> None:
    """Debe rechazar una paridad que no pertenezca a Parity."""
    with pytest.raises(TypeError, match="parity"):
        UartConfig(
            baudrate=9600,
            parity="N",  # type: ignore[arg-type]
            stop_bits=StopBits.ONE,
            timeout=1.0,
        )


def test_rejects_invalid_stop_bits() -> None:
    """Debe rechazar bits de parada que no pertenezcan a StopBits."""
    with pytest.raises(TypeError, match="stop_bits"):
        UartConfig(
            baudrate=9600,
            parity=Parity.NONE,
            stop_bits=1,  # type: ignore[arg-type]
            timeout=1.0,
        )


def test_rejects_negative_timeout() -> None:
    """Debe rechazar un tiempo de espera negativo."""
    with pytest.raises(ValueError, match="timeout"):
        UartConfig(
            baudrate=9600,
            parity=Parity.NONE,
            stop_bits=StopBits.ONE,
            timeout=-1.0,
        )