import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_app_config
from app.exceptions import SensorAlreadyExistsError
from app.observability import (
    MetricsSnapshot,
    ObservabilityMiddleware,
    configure_logging,
    log_event,
    metrics_collector,
)
from app.routers.alerts import router as alerts_router
from app.routers.readings import router as readings_router
from app.routers.sensors import router as sensors_router

config = get_app_config()
logger = configure_logging(config.log_level)

app = FastAPI(title=config.app_name, version=config.app_version)
app.add_middleware(
    ObservabilityMiddleware,
    collector=metrics_collector,
    logger=logger,
)

app.include_router(sensors_router)
app.include_router(readings_router)
app.include_router(alerts_router)


def _log_application_error(
    request: Request,
    error: Exception,
    detail: str,
    level: int = logging.WARNING,
) -> None:
    log_event(
        logger,
        level,
        "application_error",
        error_type=type(error).__name__,
        path=request.url.path,
        detail=detail,
    )


@app.exception_handler(SensorAlreadyExistsError)
async def sensor_already_exists_handler(
    request: Request,
    error: SensorAlreadyExistsError,
) -> JSONResponse:
    """Convierte duplicados de sensores en conflictos HTTP."""

    detail = str(error)
    _log_application_error(request, error, detail)
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": detail},
    )


@app.exception_handler(LookupError)
async def lookup_error_handler(
    request: Request,
    error: LookupError,
) -> JSONResponse:
    """Convierte búsquedas fallidas en respuestas 404."""

    detail = str(error)
    _log_application_error(request, error, detail)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": detail},
    )


@app.exception_handler(ValueError)
async def value_error_handler(
    request: Request,
    error: ValueError,
) -> JSONResponse:
    """Convierte errores de entrada del dominio en respuestas 400."""

    detail = str(error)
    _log_application_error(request, error, detail)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": detail},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(
    request: Request,
    error: SQLAlchemyError,
) -> JSONResponse:
    """Oculta detalles de persistencia y señala indisponibilidad."""

    detail = "Error de persistencia"
    _log_application_error(request, error, detail, logging.ERROR)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": detail},
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    """Evita exponer detalles de excepciones inesperadas."""

    detail = "Error interno del servidor"
    _log_application_error(request, error, detail, logging.ERROR)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": detail},
    )


@app.get(
    "/health",
    tags=["health"],
)
def health_check() -> dict[str, str]:
    """Indica que la aplicación está disponible."""

    return {"status": "ok"}


@app.get(
    "/metrics",
    tags=["metrics"],
)
def metrics() -> MetricsSnapshot:
    """Expone contadores básicos del proceso sin consultar la base de datos."""

    return metrics_collector.snapshot()
