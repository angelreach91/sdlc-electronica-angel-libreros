from dataclasses import dataclass
from enum import Enum
from math import isfinite


class Parity(Enum):
    """Opciones de paridad admitidas por la configuración UART."""

    NONE = "N"
    EVEN = "E"
    ODD = "O"


class StopBits(Enum):
    """Cantidades admitidas de bits de parada."""

    ONE = 1
    TWO = 2


def _validate_baudrate(value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("baudrate debe ser un entero, no un booleano")
    if value <= 0:
        raise ValueError("baudrate debe ser mayor que cero")


def _validate_parity(value: object) -> None:
    if not isinstance(value, Parity):
        raise TypeError("parity debe ser un miembro de Parity")


def _validate_stop_bits(value: object) -> None:
    if not isinstance(value, StopBits):
        raise TypeError("stop_bits debe ser un miembro de StopBits")


def _validate_timeout(value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("timeout debe ser numérico, no booleano")
    if value < 0 or not isfinite(value):
        raise ValueError("timeout debe ser finito y no negativo")


@dataclass(frozen=True)
class UartConfig:
    """Configuración inmutable de un dispositivo UART."""

    baudrate: int
    parity: Parity
    stop_bits: StopBits
    timeout: float

    def __post_init__(self) -> None:
        _validate_baudrate(self.baudrate)
        _validate_parity(self.parity)
        _validate_stop_bits(self.stop_bits)
        _validate_timeout(self.timeout)
