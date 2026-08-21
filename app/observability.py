import json
import logging
import time
from threading import Lock
from typing import TypedDict

from starlette.types import ASGIApp, Message, Receive, Scope, Send


class MetricsSnapshot(TypedDict):
    """Vista consistente de los contadores de ejecución."""

    requests_total: int
    errors_total: int
    uptime_seconds: float


class MetricsCollector:
    """Mantiene métricas básicas en memoria de forma segura."""

    def __init__(self) -> None:
        self._requests_total = 0
        self._errors_total = 0
        self._started_at = time.monotonic()
        self._lock = Lock()

    def record_request(self, status_code: int) -> None:
        """Registra una respuesta HTTP y si terminó con error."""

        with self._lock:
            self._requests_total += 1
            if status_code >= 400:
                self._errors_total += 1

    def snapshot(self) -> MetricsSnapshot:
        """Obtiene un corte consistente de las métricas actuales."""

        with self._lock:
            requests_total = self._requests_total
            errors_total = self._errors_total

        return {
            "requests_total": requests_total,
            "errors_total": errors_total,
            "uptime_seconds": max(0.0, time.monotonic() - self._started_at),
        }


class JsonFormatter(logging.Formatter):
    """Convierte eventos de aplicación en objetos JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Serializa el evento y sus campos adicionales."""

        payload: dict[str, object] = {"event": record.getMessage()}
        event_fields = getattr(record, "event_fields", {})

        if isinstance(event_fields, dict):
            payload.update(event_fields)

        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level_name: str) -> logging.Logger:
    """Configura el logger de SensorHub con salida JSON."""

    logger = logging.getLogger("sensorhub")
    level = getattr(logging, level_name.upper(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    if not any(
        handler.get_name() == "sensorhub-json"
        for handler in logger.handlers
    ):
        handler = logging.StreamHandler()
        handler.set_name("sensorhub-json")
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    **fields: object,
) -> None:
    """Emite un evento que será serializado por ``JsonFormatter``."""

    logger.log(
        level,
        event,
        extra={"event_fields": fields},
    )


class ObservabilityMiddleware:
    """Registra métricas y un evento JSON por petición HTTP."""

    def __init__(
        self,
        app: ASGIApp,
        collector: MetricsCollector,
        logger: logging.Logger,
    ) -> None:
        self.app = app
        self.collector = collector
        self.logger = logger

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        started_at = time.monotonic()
        status_code = 500

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            self._record_request(scope, 500, started_at)
            raise

        self._record_request(scope, status_code, started_at)

    def _record_request(
        self,
        scope: Scope,
        status_code: int,
        started_at: float,
    ) -> None:
        self.collector.record_request(status_code)
        log_event(
            self.logger,
            logging.INFO,
            "http_request",
            method=scope["method"],
            path=scope["path"],
            status_code=status_code,
            duration_ms=round(
                (time.monotonic() - started_at) * 1000,
                2,
            ),
        )


metrics_collector = MetricsCollector()
