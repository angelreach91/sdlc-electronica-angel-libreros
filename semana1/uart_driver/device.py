from typing import Protocol

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser, ParsedMessage


class MessageBuffer(Protocol):
    """Representa un destino para mensajes procesados."""

    def append(self, item: ParsedMessage) -> None:
        ...


class UartDevice:
    """Coordina el estado de una UART y el análisis de sus tramas."""

    def __init__(
        self,
        config: UartConfig,
        parser: MessageParser,
        buffer: MessageBuffer | None = None,
    ) -> None:
        self._config = config
        self._parser = parser
        self._buffer: MessageBuffer | None = buffer
        self._is_connected = False

    @property
    def config(self) -> UartConfig:
        """Devuelve la configuración inyectada."""
        return self._config

    @property
    def is_connected(self) -> bool:
        """Indica si el dispositivo está conectado lógicamente."""
        return self._is_connected

    def connect(self) -> None:
        """Conecta lógicamente el dispositivo."""
        self._is_connected = True

    def disconnect(self) -> None:
        """Desconecta lógicamente el dispositivo."""
        self._is_connected = False

    def read_and_parse(self, frame: bytes) -> ParsedMessage:
        """Valida y procesa una trama mediante el parser inyectado."""
        if not self._is_connected:
            raise RuntimeError("El dispositivo no está conectado.")

        if not self._parser.can_parse(frame):
            raise ValueError("El parser no reconoce la trama recibida.")

        result: ParsedMessage = self._parser.parse(frame)

        if self._buffer is not None:
            self._buffer.append(result)

        return result
