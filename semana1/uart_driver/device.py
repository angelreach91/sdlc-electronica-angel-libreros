from logging import Logger
from typing import Protocol

from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser, ParsedMessage


class MessageBuffer(Protocol):
    """Representa un destino para mensajes procesados."""

    def append(self, item: ParsedMessage) -> None:
        """Almacena un mensaje procesado."""
        ...


class UartDevice:
    """Coordina el estado, parsing y eventos de una UART."""

    def __init__(
        self,
        config: UartConfig,
        parser: MessageParser,
        buffer: MessageBuffer | None = None,
        logger: Logger | None = None,
    ) -> None:
        self._config = config
        self._parser = parser
        self._buffer: MessageBuffer | None = buffer
        self._logger: Logger | None = logger
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

        if self._logger is not None:
            self._logger.info("uart.connected")

    def disconnect(self) -> None:
        """Desconecta lógicamente el dispositivo."""
        self._is_connected = False

        if self._logger is not None:
            self._logger.info("uart.disconnected")

    def read_and_parse(self, frame: bytes) -> ParsedMessage:
        """Valida y procesa una trama mediante el parser inyectado."""
        if not self._is_connected:
            if self._logger is not None:
                self._logger.warning("uart.read_rejected")

            raise RuntimeError("El dispositivo no está conectado.")

        if not self._parser.can_parse(frame):
            if self._logger is not None:
                self._logger.warning("uart.frame_unrecognized")

            raise ValueError("El parser no reconoce la trama recibida.")

        result: ParsedMessage = self._parser.parse(frame)

        if self._buffer is not None:
            self._buffer.append(result)

        if self._logger is not None:
            self._logger.info("uart.frame_parsed")

        return result