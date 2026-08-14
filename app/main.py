from fastapi import FastAPI

from app.routers.alerts import router as alerts_router
from app.routers.readings import router as readings_router
from app.routers.sensors import router as sensors_router

app = FastAPI(
    title="SensorHub",
    version="0.2.0",
)

app.include_router(sensors_router)
app.include_router(readings_router)
app.include_router(alerts_router)


@app.get(
    "/health",
    tags=["health"],
)
def health_check() -> dict[str, str]:
    """Indica que la aplicación está disponible."""

    return {"status": "ok"}
