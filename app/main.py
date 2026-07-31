from fastapi import FastAPI

from app.routers.readings import router as readings_router

app = FastAPI(title="SensorHub")

app.include_router(readings_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Indica que la aplicación está disponible."""

    return {"status": "ok"}