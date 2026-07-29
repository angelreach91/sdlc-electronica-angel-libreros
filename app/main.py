from datetime import UTC, datetime

from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class ReadingInput(BaseModel):
    sensor_id: str = Field(min_length=1)
    temperature: float
    humidity: float = Field(ge=0, le=100)


class ReadingResponse(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    received_at: datetime


app = FastAPI(title="SensorHub")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(reading: ReadingInput) -> ReadingResponse:
    return ReadingResponse(
        sensor_id=reading.sensor_id,
        temperature=reading.temperature,
        humidity=reading.humidity,
        received_at=datetime.now(UTC),
    )
