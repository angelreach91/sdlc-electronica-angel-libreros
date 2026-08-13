# Prompting efectivo — Semana 5

## Objetivo

Comparar los resultados obtenidos mediante prompts poco específicos y prompts estructurados al solicitar tareas de programación relacionadas con **SensorHub**.

Para los prompts estructurados se utilizará la siguiente organización:

- **Contexto:** qué sistema se está desarrollando y qué tecnologías utiliza.
- **Tarea:** qué se solicita realizar exactamente.
- **Restricciones:** condiciones que debe respetar la solución.
- **Entrega:** formato esperado de la respuesta.

---

## Tarea 1 — Endpoint POST para registrar una lectura

### Prompt pobre

> Crea un endpoint POST para registrar una lectura de un sensor.

### Resultado del prompt pobre

```python
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- DB setup (SQLite para ejemplo) ---
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# --- SQLAlchemy model ---
class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    metadata = Column(JSON, nullable=True)

Base.metadata.create_all(bind=engine)

# --- Pydantic schemas ---
class ReadingCreate(BaseModel):
    sensor_id: str = Field(..., min_length=1, example="sensor-123")
    value: float = Field(..., example=23.7)
    unit: Optional[str] = Field(None, example="°C")
    timestamp: Optional[datetime] = Field(
        None,
        example="2026-08-13T12:34:56Z",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        example={"battery": 87},
    )

    @validator("timestamp", pre=True, always=True)
    def set_now_if_missing(cls, v):
        return v or datetime.utcnow()

class ReadingOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    unit: Optional[str]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True

# --- FastAPI app ---
app = FastAPI(title="Sensor Readings API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/readings",
    response_model=ReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    payload: ReadingCreate,
    db: Session = Depends(get_db),
):
    # Basic validation (example: value must be finite)
    if payload.value is None:
        raise HTTPException(
            status_code=400,
            detail="value is required",
        )

    # Create DB object
    db_reading = Reading(
        sensor_id=payload.sensor_id,
        value=payload.value,
        unit=payload.unit,
        timestamp=payload.timestamp,
        metadata=payload.metadata,
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading
```

### Prompt estructurado

> **CONTEXTO:** Estoy desarrollando SensorHub, una API REST con FastAPI y Python 3.12 para gestionar sensores y sus lecturas. El proyecto utiliza arquitectura en capas: `routers -> services -> repositories -> models`. La lógica de negocio debe permanecer en `ReadingService` y los routers no deben acceder directamente a SQLAlchemy.
>
> **TAREA:** Escribe un endpoint POST para registrar una nueva lectura en la ruta `/sensors/{sensor_id}/readings`.
>
> El endpoint debe recibir un `ReadingCreate` con los campos `value` y `unit`, llamar a `ReadingService.create_reading()` y devolver un `ReadingResponse`.
>
> **RESTRICCIONES:**
>
> - Usa `APIRouter`.
> - Inyecta `ReadingService` mediante `ReadingServiceDependency`.
> - Usa `response_model=ReadingResponse`.
> - Devuelve HTTP `201 Created` cuando la lectura se registre correctamente.
> - Convierte `LookupError` en HTTP `404`.
> - Convierte `ValueError` en HTTP `400`.
> - No accedas directamente al repositorio ni a SQLAlchemy.
> - No implementes reglas de negocio dentro del router.
> - No crees ni reescribas modelos, schemas, servicios o repositorios.
> - Mantén `type hints` completos.
>
> **ENTREGA:** Devuelve únicamente la función del endpoint con su decorador, sin modificar otros archivos y sin explicaciones adicionales.

### Resultado del prompt estructurado

```python
@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_reading(
    sensor_id: int,
    reading_in: ReadingCreate,
    service: ReadingService = Depends(ReadingServiceDependency),
) -> ReadingResponse:
    try:
        created_reading: ReadingResponse = await service.create_reading(
            sensor_id,
            reading_in,
        )
        return created_reading
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
```

### Comparación

La diferencia entre ambos resultados muestra con mayor claridad el efecto de proporcionar contexto y restricciones en una tarea relacionada con una API REST.

Con el prompt pobre, Copilot tuvo que decidir prácticamente toda la estructura de la solución. Aunque la solicitud únicamente pedía un endpoint POST, la respuesta creó una pequeña aplicación completa con FastAPI, configuración de SQLite, sesiones de SQLAlchemy, un modelo ORM, schemas de Pydantic y una dependencia para acceder directamente a la base de datos.

También inventó elementos que no corresponden con SensorHub. Por ejemplo, utilizó la ruta `/readings`, colocó `sensor_id` dentro del cuerpo de la petición, agregó campos como `timestamp` y `metadata`, utilizó un schema llamado `ReadingOut` y realizó directamente `add()`, `commit()` y `refresh()` desde el endpoint.

Esto rompe la separación de responsabilidades utilizada en el proyecto, ya que en SensorHub el router no debe gestionar directamente la persistencia. Su responsabilidad es recibir la petición y delegar la lógica de negocio a `ReadingService`, mientras que el acceso a SQLAlchemy pertenece a la capa de repositorios.

El prompt estructurado redujo considerablemente estas suposiciones. Copilot respetó la ruta `/sensors/{sensor_id}/readings`, utilizó `ReadingCreate` y `ReadingResponse`, devolvió HTTP `201 Created`, utilizó un servicio y contempló la transformación de `LookupError` en `404` y `ValueError` en `400`. También dejó de generar modelos, schemas, configuración de base de datos y código de persistencia innecesario.

Sin embargo, el resultado estructurado todavía presentó errores que deben detectarse mediante revisión humana. Definió `sensor_id` como `int`, aunque SensorHub utiliza identificadores de tipo `str`. También convirtió el endpoint en asíncrono y utilizó `await`, aunque `ReadingService.create_reading()` es un método síncrono.

Además, realizó la llamada `service.create_reading(sensor_id, reading_in)`, pero el contrato real del servicio recibe por separado `sensor_id`, `value` y `unit`. También intentó envolver `ReadingServiceDependency` nuevamente mediante `Depends()`, aunque en el proyecto esta dependencia ya está definida mediante un alias y se utiliza directamente como anotación.

Por lo tanto, el prompt estructurado produjo una solución mucho más cercana a la arquitectura real de SensorHub, pero no una solución que deba aceptarse automáticamente. El ejercicio demuestra que proporcionar contexto, una tarea concreta, restricciones y un formato de entrega reduce considerablemente las decisiones que la IA debe inventar, pero la revisión humana sigue siendo necesaria para detectar diferencias con los contratos reales del sistema.

---

## Tarea 2 — Endpoint GET con filtros y paginación

### Prompt pobre

> Haz un endpoint GET para consultar las lecturas de un sensor con filtros.

### Resultado del prompt pobre

```javascript
// Uso: requiere express y pg Pool ya configurado.
// Ejemplo: const pool = new Pool({ connectionString: process.env.DATABASE_URL });
//          const router = require('./routes/sensorReadings')(pool);

const express = require('express');

module.exports = function (pool) {
  const router = express.Router();

  // GET /sensors/:sensorId/readings
  // Query params soportados:
  // from (ISO8601), to (ISO8601), min (numeric), max (numeric),
  // limit (int, default 100, max 1000), offset (int), sort (asc|desc, default desc)
  router.get('/sensors/:sensorId/readings', async (req, res) => {
    try {
      const { sensorId } = req.params;
      const {
        from,
        to,
        min,
        max,
        limit = '100',
        offset = '0',
        sort = 'desc',
      } = req.query;

      // Validaciones básicas
      if (!/^\d+$/.test(sensorId)) {
        return res.status(400).json({ error: 'sensorId inválido' });
      }

      const parsedLimit = Math.min(
        Math.max(parseInt(limit, 10) || 100, 1),
        1000
      );
      const parsedOffset = Math.max(parseInt(offset, 10) || 0, 0);
      const sortLower = (sort || 'desc').toLowerCase();

      if (!['asc', 'desc'].includes(sortLower)) {
        return res
          .status(400)
          .json({ error: 'sort debe ser "asc" o "desc"' });
      }

      const params = [];
      let idx = 1;

      // sensorId como primer parámetro
      params.push(sensorId);

      let where = 'WHERE sensor_id = $' + idx++;

      // from / to
      if (from) {
        const fromDate = new Date(from);

        if (isNaN(fromDate.getTime())) {
          return res.status(400).json({ error: 'from inválido' });
        }

        params.push(fromDate.toISOString());
        where += ' AND timestamp >= $' + idx++;
      }

      if (to) {
        const toDate = new Date(to);

        if (isNaN(toDate.getTime())) {
          return res.status(400).json({ error: 'to inválido' });
        }

        params.push(toDate.toISOString());
        where += ' AND timestamp <= $' + idx++;
      }

      // min / max valores
      if (min !== undefined) {
        const n = Number(min);

        if (Number.isNaN(n)) {
          return res.status(400).json({ error: 'min inválido' });
        }

        params.push(n);
        where += ' AND value >= $' + idx++;
      }

      if (max !== undefined) {
        const n = Number(max);

        if (Number.isNaN(n)) {
          return res.status(400).json({ error: 'max inválido' });
        }

        params.push(n);
        where += ' AND value <= $' + idx++;
      }

      // Construcción final de la query
      const queryText = `
        SELECT id, sensor_id, value, timestamp
        FROM sensor_readings
        ${where}
        ORDER BY timestamp ${sortLower}
        LIMIT $${idx++}
        OFFSET $${idx++}
      `;

      params.push(parsedLimit, parsedOffset);

      const { rows } = await pool.query(queryText, params);

      return res.json({ data: rows });
    } catch (err) {
      console.error('Error consultando lecturas:', err);
      return res.status(500).json({ error: 'error interno' });
    }
  });

  return router;
};
```

### Prompt estructurado

> **CONTEXTO:** Estoy desarrollando SensorHub, una API REST con FastAPI y Python 3.12. El proyecto utiliza arquitectura en capas: `routers -> services -> repositories -> models`. La lógica de negocio y las consultas a persistencia deben permanecer fuera del router.
>
> **TAREA:** Escribe un endpoint GET para consultar el historial de lecturas de un sensor mediante la ruta `/sensors/{sensor_id}/readings`.
>
> El endpoint debe aceptar:
>
> - `sensor_id` como parámetro de ruta.
> - `limit` como query parameter, con valor por defecto 50, mínimo 1 y máximo 100.
> - `offset` como query parameter, con valor por defecto 0 y mínimo 0.
> - `from` como fecha inicial opcional.
> - `to` como fecha final opcional.
>
> **RESTRICCIONES:**
>
> - Usa `APIRouter`.
> - Inyecta `ReadingService` mediante `ReadingServiceDependency`.
> - Usa `response_model=list[ReadingResponse]`.
> - Usa `Annotated` y `Query` para validar `limit` y `offset`.
> - Los parámetros HTTP `from` y `to` deben mapearse internamente a `from_date` y `to_date`.
> - Llama a `ReadingService.list_by_sensor()`.
> - Convierte `LookupError` en HTTP `404`.
> - Convierte `ValueError` en HTTP `400`.
> - No escribas consultas SQL dentro del endpoint.
> - No accedas directamente al repositorio.
> - No implementes reglas de negocio en el router.
> - No crees ni reescribas modelos, schemas, servicios o repositorios.
> - Mantén `type hints` completos.
>
> **ENTREGA:** Devuelve únicamente la función del endpoint con su decorador, sin explicaciones adicionales.

### Resultado del prompt estructurado

```python
@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[ReadingResponse],
)
async def get_sensor_readings(
    sensor_id: int,
    limit: Annotated[int, Query(50, ge=1, le=100)],
    offset: Annotated[int, Query(0, ge=0)],
    from_date: Annotated[
        datetime.datetime | None,
        Query(None, alias="from"),
    ] = None,
    to_date: Annotated[
        datetime.datetime | None,
        Query(None, alias="to"),
    ] = None,
    reading_service: ReadingService = Depends(
        ReadingServiceDependency
    ),
) -> list[ReadingResponse]:
    try:
        return await reading_service.list_by_sensor(
            sensor_id=sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
```

### Comparación

La diferencia entre ambos resultados es mucho más evidente que en una tarea sencilla. Con el prompt pobre, Copilot no recibió información sobre el lenguaje, framework, arquitectura ni contratos existentes, por lo que tuvo que tomar todas esas decisiones por su cuenta.

La respuesta utilizó JavaScript con Express y PostgreSQL mediante `pg`, aunque SensorHub está desarrollado con Python y FastAPI. También escribió la consulta SQL directamente dentro del endpoint, mezclando las responsabilidades del router con la persistencia. Además, inventó filtros `min`, `max` y `sort`, estableció un límite máximo de 1000 registros, asumió que `sensorId` debía ser numérico y creó nombres como `sensor_readings` y `timestamp` que no fueron especificados.

El código generado no necesariamente sería incorrecto en otro proyecto, pero no corresponde con la arquitectura ni con los contratos existentes de SensorHub. Esto demuestra que, ante una solicitud ambigua, la IA puede construir una solución funcional alrededor de supuestos completamente distintos a los del sistema real.

El prompt estructurado redujo considerablemente esa ambigüedad. Copilot utilizó FastAPI, respetó la ruta `/sensors/{sensor_id}/readings`, incluyó los parámetros `limit`, `offset`, `from` y `to`, empleó `ReadingResponse` como modelo de salida y delegó la consulta a `ReadingService.list_by_sensor()` en lugar de escribir SQL directamente dentro del router. También contempló la transformación de `LookupError` en HTTP `404` y de `ValueError` en HTTP `400`.

Sin embargo, el resultado estructurado todavía requirió revisión. Copilot definió `sensor_id` como `int`, mientras que SensorHub utiliza identificadores de tipo `str`. También convirtió el endpoint en asíncrono y utilizó `await` sobre `ReadingService.list_by_sensor()`, aunque el servicio actual es síncrono. Además, intentó inyectar `ReadingServiceDependency` mediante un `Depends()` adicional, aunque esa dependencia ya se encuentra definida en el alias utilizado por el proyecto.

Por lo tanto, el prompt estructurado produjo una solución mucho más cercana a la arquitectura real, pero no eliminó completamente los errores. Esto demuestra que mejorar el prompt reduce las suposiciones y orienta mejor a la IA, pero el código generado debe seguir tratándose como una propuesta que necesita revisión y criterio técnico antes de incorporarse al proyecto.

---

## Tarea 3 — Endpoint POST para registrar un sensor

### Prompt pobre

> Crea un endpoint POST para registrar un sensor.

### Resultado del prompt pobre

```python
from typing import Optional, Dict
from uuid import uuid4
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import (
    SQLModel,
    Field as ORMField,
    create_engine,
    Session,
    select,
    JSON,
)

# Modelos Pydantic / SQLModel
class SensorCreate(BaseModel):
    uuid: Optional[str] = Field(
        None,
        description="UUID del sensor; si se omite se genera uno",
    )
    name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    location: Optional[str] = None
    metadata: Optional[Dict] = None


class Sensor(SQLModel, table=True):
    id: Optional[int] = ORMField(default=None, primary_key=True)
    uuid: str = ORMField(index=True, unique=True)
    name: str
    type: str
    location: Optional[str] = None
    metadata: Optional[JSON] = None
    created_at: datetime = ORMField(default_factory=datetime.utcnow)


# DB setup (SQLite para ejemplo)
DATABASE_URL = "sqlite:///./sensors.db"
engine = create_engine(DATABASE_URL, echo=False)
SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.post(
    "/sensors",
    status_code=status.HTTP_201_CREATED,
    response_model=Sensor,
)
def create_sensor(payload: SensorCreate):
    sensor_uuid = payload.uuid or str(uuid4())

    with Session(engine) as session:
        # comprobar duplicado por uuid o por nombre (según reglas)
        q = select(Sensor).where(
            (Sensor.uuid == sensor_uuid)
            | (Sensor.name == payload.name)
        )
        existing = session.exec(q).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sensor ya existe (uuid o nombre duplicado)",
            )

        sensor = Sensor(
            uuid=sensor_uuid,
            name=payload.name,
            type=payload.type,
            location=payload.location,
            metadata=payload.metadata,
        )

        session.add(sensor)
        session.commit()
        session.refresh(sensor)

        return sensor
```

### Prompt estructurado

> **CONTEXTO:** Estoy desarrollando SensorHub, una API REST con FastAPI y Python 3.12. El proyecto utiliza arquitectura en capas: `routers -> services -> repositories -> models`. La lógica de negocio debe permanecer en `SensorService` y los routers no deben acceder directamente a SQLAlchemy ni a los repositorios.
>
> **TAREA:** Escribe un endpoint POST para registrar un nuevo sensor mediante la ruta `/sensors`.
>
> El endpoint debe recibir un `SensorCreate` que contiene:
>
> - `id`
> - `name`
> - `sensor_type`
> - `unit`
>
> Debe utilizar `SensorService` para registrar el sensor y devolver un `SensorResponse`.
>
> **RESTRICCIONES:**
>
> - Usa `APIRouter`.
> - Usa `response_model=SensorResponse`.
> - Devuelve HTTP `201 Created` cuando el sensor se registre correctamente.
> - Inyecta `SensorService` mediante `SensorServiceDependency`.
> - Usa `SensorServiceDependency` directamente como anotación de la dependencia.
> - Llama a `SensorService.create_sensor()`.
> - Pasa `id`, `name`, `sensor_type` y `unit` por separado al servicio.
> - Si se produce `SensorAlreadyExistsError`, responde HTTP `409 Conflict`.
> - Si se produce `ValueError`, responde HTTP `400 Bad Request`.
> - No accedas directamente a SQLAlchemy.
> - No accedas directamente al repositorio.
> - No implementes reglas de negocio dentro del router.
> - No crees ni reescribas modelos, schemas, servicios o repositorios.
> - Mantén el endpoint síncrono.
> - Mantén `type hints` completos.
>
> **ENTREGA:** Devuelve únicamente la función del endpoint con su decorador, sin imports, explicaciones ni modificaciones a otros componentes.

### Resultado del prompt estructurado

```python
@router.post(
    "/sensors",
    response_model=SensorResponse,
    status_code=201,
)
def create_sensor(
    sensor_create: SensorCreate,
    service: SensorServiceDependency = Depends(
        SensorServiceDependency
    ),
) -> SensorResponse:
    try:
        sensor = service.create_sensor(
            sensor_create.id,
            sensor_create.name,
            sensor_create.sensor_type,
            sensor_create.unit,
        )
        return sensor
    except SensorAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
```

### Comparación

El prompt pobre volvió a demostrar que una instrucción corta puede obligar a la IA a tomar decisiones que deberían pertenecer al diseño del proyecto. Al no recibir información sobre SensorHub, Copilot creó su propia solución completa alrededor del endpoint.

La respuesta eligió `SQLModel`, creó una base SQLite, definió nuevamente los modelos y accedió directamente a la sesión de persistencia desde el endpoint. También inventó campos como `uuid`, `location`, `metadata` y `created_at`, además de decidir automáticamente que se debía generar un UUID cuando no fuera proporcionado.

Incluso creó una regla de negocio propia para considerar duplicado un sensor cuando coincidiera su UUID o su nombre. Ninguna de esas decisiones había sido especificada en el prompt.

Esto provocó que el endpoint mezclara distintas responsabilidades. La misma función valida duplicados, consulta la base de datos, crea el objeto persistente, ejecuta `add()`, `commit()` y `refresh()` y finalmente construye la respuesta. Esa organización no corresponde con la arquitectura en capas utilizada por SensorHub.

El prompt estructurado redujo considerablemente estas suposiciones. Copilot dejó de crear modelos y configuración de persistencia, utilizó `SensorCreate` y `SensorResponse`, delegó el registro a `SensorService.create_sensor()` y pasó por separado `id`, `name`, `sensor_type` y `unit`. También contempló correctamente HTTP `201` para la creación, `409` cuando ocurre `SensorAlreadyExistsError` y `400` cuando ocurre `ValueError`.

Sin embargo, incluso con instrucciones explícitas todavía fue necesaria una revisión humana. El prompt indicaba que `SensorServiceDependency` debía utilizarse directamente como anotación, pero Copilot volvió a envolverla mediante `Depends(SensorServiceDependency)`.

También declaró que la función devuelve `SensorResponse`, pero retorna directamente el objeto producido por `SensorService.create_sensor()`. En la implementación actual de SensorHub, el objeto del dominio se transforma explícitamente mediante `SensorResponse.model_validate(sensor)` antes de ser devuelto.

Además, el router real de sensores ya posee el prefijo `/sensors`, por lo que dentro de esa estructura el decorador utiliza una ruta vacía en lugar de repetir `/sensors`. El código generado entiende correctamente la ruta HTTP solicitada, pero todavía necesitaría adaptarse al contexto concreto del router existente antes de incorporarse al proyecto.

Esta tercera comparación confirma el mismo patrón observado en las tareas anteriores: el prompt estructurado limita considerablemente las decisiones que la IA debe inventar y produce código mucho más cercano a la arquitectura deseada, pero no garantiza que la respuesta sea directamente integrable. El desarrollador sigue siendo responsable de revisar contratos, dependencias, tipos y convenciones del proyecto antes de aceptar el código generado.

---

## Conclusión

Las tres tareas permitieron observar con mayor claridad cómo influye la calidad del prompt cuando se trabaja con código más cercano a un proyecto real. En los prompts pobres, Copilot tuvo que completar por su cuenta información que no fue especificada, como el lenguaje, el framework, la estructura de la aplicación, los modelos, la persistencia y algunas reglas de negocio. Esto produjo soluciones que podían ser funcionales de manera aislada, pero que no necesariamente respetaban la arquitectura ni los contratos existentes de SensorHub.

En cambio, los prompts estructurados redujeron considerablemente esa ambigüedad al proporcionar contexto, una tarea concreta, restricciones y un formato de entrega. Las respuestas se acercaron mucho más a la arquitectura utilizada en el proyecto, respetando mejor la separación entre routers, servicios y repositorios, además de los modelos y códigos HTTP esperados.

Aun así, los resultados estructurados no fueron perfectos. Copilot todavía introdujo diferencias en tipos, dependencias, llamadas a métodos y convenciones del proyecto. Esto confirma que un buen prompt mejora la precisión y la consistencia de la respuesta, pero no sustituye la revisión del desarrollador.

La principal conclusión es que la IA funciona mejor cuando recibe instrucciones claras y límites definidos. Mientras más compleja es la tarea, más importante resulta especificar el contexto y las restricciones, ya que cualquier decisión que no se indique explícitamente puede ser asumida o inventada por el modelo. Por ello, el código generado debe considerarse una propuesta que necesita ser revisada, entendida y validada antes de incorporarse al proyecto.