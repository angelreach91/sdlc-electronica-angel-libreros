# SensorHub

[![CI](https://github.com/angelreach91/sdlc-electronica-angel-libreros/actions/workflows/ci.yml/badge.svg)](https://github.com/angelreach91/sdlc-electronica-angel-libreros/actions/workflows/ci.yml)

SensorHub es una API REST desarrollada con FastAPI para administrar sensores y sus lecturas.

El proyecto utiliza una arquitectura en cuatro capas, persistencia con SQLAlchemy 2.x, validación mediante Pydantic, migraciones con Alembic, documentación automática con Swagger y pruebas automatizadas con Pytest.

La aplicación utiliza SQLite de manera predeterminada para la ejecución local y puede conectarse a PostgreSQL mediante la variable de entorno `DATABASE_URL`. También puede ejecutarse dentro de contenedores mediante Docker y Docker Compose.

Este repositorio conserva los ejercicios realizados durante las semanas anteriores del curso como material histórico.

## Funcionalidades

SensorHub permite:

- registrar sensores de temperatura y humedad;
- consultar sensores existentes;
- actualizar parcialmente el nombre y el estado de un sensor;
- desactivar sensores sin eliminarlos físicamente;
- registrar lecturas asociadas a un sensor;
- consultar lecturas mediante identificador;
- listar lecturas con paginación;
- filtrar lecturas por rango de fechas;
- actualizar lecturas;
- eliminar lecturas;
- rechazar datos que no respeten las reglas físicas definidas;
- impedir que el tipo y la unidad de un sensor cambien después de su creación;
- responder con `409 Conflict` cuando se intenta registrar un identificador existente.

## Tipos de sensor

### Temperatura

- Tipo: `temperature`
- Unidad válida: `C`
- Valor mínimo: `-273.15`

### Humedad

- Tipo: `humidity`
- Unidad válida: `%`
- Intervalo permitido: `0` a `100`

La API también rechaza lecturas cuando:

- el sensor no existe;
- el sensor está desactivado;
- la unidad no corresponde al tipo de sensor;
- el valor se encuentra fuera del rango físico permitido.

## Arquitectura

La aplicación sigue el siguiente flujo:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Model
  ↓
SQLite o PostgreSQL
```

### Routers

Reciben las solicitudes HTTP, delegan las operaciones y generan las respuestas correspondientes.

Archivos principales:

- `app/routers/sensors.py`
- `app/routers/readings.py`

### Services

Contienen las reglas de negocio y coordinan las operaciones.

Archivos principales:

- `app/services/sensor_service.py`
- `app/services/reading_service.py`

### Repositories

Administran el acceso a los datos mediante SQLAlchemy.

Archivos principales:

- `app/repositories/sensor_repository.py`
- `app/repositories/reading_repository.py`

### Models

Representan las tablas de la base de datos mediante la API tipada de SQLAlchemy 2.x.

Archivos principales:

- `app/models/sensor.py`
- `app/models/reading.py`

### Schemas

Definen los contratos de entrada y salida mediante Pydantic.

Archivos principales:

- `app/schemas/sensor.py`
- `app/schemas/reading.py`

## Estructura principal

```text
app/
├── main.py
├── db.py
├── dependencies.py
├── exceptions.py
├── sensor_types.py
├── models/
├── repositories/
├── routers/
├── schemas/
└── services/

migrations/
├── versions/
├── env.py
└── script.py.mako

tests/
docs/adr/
semana1/
semana2/
AI_LOG.md
README.md
Dockerfile
docker-compose.yml
.env.example
alembic.ini
requirements.txt
pyproject.toml
```

## Instalación local

Desde la raíz del repositorio, crea un entorno virtual:

```bash
python -m venv .venv
```

En Linux o WSL, actívalo con:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Configuración de la base de datos

SensorHub obtiene la conexión mediante la variable de entorno:

```text
DATABASE_URL
```

Si la variable no está definida, la aplicación utiliza SQLite:

```text
sqlite:///./sensorhub.db
```

Por tanto, la ejecución local puede utilizar `sensorhub.db` sin configuración adicional.

Para PostgreSQL puede utilizarse una dirección con esta estructura:

```text
postgresql+psycopg://usuario:contraseña@host:5432/base_de_datos
```

La aplicación también normaliza direcciones que comienzan con:

```text
postgres://
postgresql://
```

para utilizar el controlador `psycopg`.

## Migraciones con Alembic

La estructura de la base de datos se administra mediante migraciones de Alembic.

Para aplicar todas las migraciones pendientes:

```bash
python -m alembic upgrade head
```

Para consultar la migración actualmente aplicada:

```bash
python -m alembic current
```

Para consultar el historial disponible:

```bash
python -m alembic history
```

La migración inicial crea:

- la tabla `sensors`;
- la tabla `readings`;
- la relación entre lecturas y sensores;
- el índice de `sensor_id`;
- la tabla interna `alembic_version`.

Los archivos de migración se encuentran en:

```text
migrations/versions/
```

## Ejecución local de la API

Primero aplica las migraciones:

```bash
python -m alembic upgrade head
```

Después inicia la API:

```bash
python -m uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

El estado del servicio puede comprobarse en:

```text
http://127.0.0.1:8000/health
```

## Ejecución con Docker

El `Dockerfile` utiliza:

```text
python:3.12-slim
```

La imagen instala las dependencias, copia la aplicación y las migraciones, aplica `alembic upgrade head` e inicia Uvicorn en el puerto 8000.

Construye la imagen con:

```bash
docker build -t sensorhub:dev .
```

Ejecuta un contenedor con SQLite mediante:

```bash
docker run --rm \
  -p 127.0.0.1:8000:8000 \
  sensorhub:dev
```

## Ejecución con Docker Compose y PostgreSQL

Docker Compose levanta dos servicios:

```text
api
db
```

El servicio `api` ejecuta SensorHub y el servicio `db` ejecuta PostgreSQL 16.

### Preparar las variables locales

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Después modifica la contraseña dentro de `.env`.

Ejemplo:

```text
POSTGRES_USER=sensor
POSTGRES_PASSWORD=contraseña-local
POSTGRES_DB=sensorhub
```

El archivo `.env` contiene configuración local y no se registra en Git.

### Levantar los servicios

```bash
docker compose up --build -d
```

Consulta su estado:

```bash
docker compose ps
```

Consulta los registros de la API:

```bash
docker compose logs api
```

Consulta los registros de PostgreSQL:

```bash
docker compose logs db
```

Al iniciar la API, Alembic aplica automáticamente las migraciones antes de ejecutar Uvicorn.

### Detener los servicios

Para eliminar los contenedores y la red, conservando los datos:

```bash
docker compose down
```

Para eliminar también el volumen y todos los datos de PostgreSQL:

```bash
docker compose down --volumes
```

Este último comando debe utilizarse con precaución porque elimina la base de datos local del entorno Docker.

## Persistencia de PostgreSQL

Docker Compose utiliza un volumen nombrado:

```text
pgdata
```

Este volumen conserva los datos aunque los contenedores sean eliminados y creados nuevamente.

El flujo de persistencia es:

```text
PostgreSQL
→ volumen pgdata
→ docker compose down
→ nuevos contenedores
→ datos recuperados
```

## Endpoints principales

### Sensores

| Método | Ruta | Operación |
|---|---|---|
| `POST` | `/sensors` | Crear sensor |
| `GET` | `/sensors` | Listar sensores |
| `GET` | `/sensors/{sensor_id}` | Consultar sensor |
| `PATCH` | `/sensors/{sensor_id}` | Actualizar sensor |
| `DELETE` | `/sensors/{sensor_id}` | Desactivar sensor |

### Lecturas

| Método | Ruta | Operación |
|---|---|---|
| `POST` | `/sensors/{sensor_id}/readings` | Crear lectura |
| `GET` | `/sensors/{sensor_id}/readings` | Listar lecturas |
| `GET` | `/readings/{reading_id}` | Consultar lectura |
| `PATCH` | `/readings/{reading_id}` | Actualizar lectura |
| `DELETE` | `/readings/{reading_id}` | Eliminar lectura |

### Estado del servicio

| Método | Ruta | Operación |
|---|---|---|
| `GET` | `/health` | Comprobar disponibilidad |

## Ejemplo de registro de un sensor

Solicitud:

```json
{
  "id": "TEMP-01",
  "name": "Sensor exterior",
  "sensor_type": "temperature",
  "unit": "C"
}
```

Respuesta esperada:

```json
{
  "id": "TEMP-01",
  "name": "Sensor exterior",
  "sensor_type": "temperature",
  "unit": "C",
  "is_active": true
}
```

## Ejemplo de registro de una lectura

Ruta:

```text
POST /sensors/TEMP-01/readings
```

Solicitud:

```json
{
  "value": 24.5,
  "unit": "C"
}
```

El flujo interno es:

```text
Solicitud HTTP
→ Router
→ Schema Pydantic
→ Service
→ Repository
→ Modelo SQLAlchemy
→ SQLite o PostgreSQL
→ Respuesta HTTP
```

## Verificaciones

Ejecuta la suite completa:

```bash
python -m pytest
```

Ejecuta las pruebas sin cobertura:

```bash
python -m pytest --no-cov -q
```

Revisa el formato y las reglas de calidad:

```bash
python -m ruff check app tests migrations
```

Comprueba el tipado:

```bash
mypy app
```

Valida la configuración de Docker Compose sin mostrar los valores expandidos:

```bash
docker compose config > /dev/null && echo "Configuración válida"
```

Consulta la migración aplicada dentro del contenedor:

```bash
docker compose exec api python -m alembic current
```

Estado verificado después de incorporar Docker Compose, PostgreSQL y Alembic:

```text
57 pruebas aprobadas
Cobertura total: 87.89 %
Ruff: sin errores
Mypy: sin errores
Docker Compose: API y PostgreSQL funcionando
PostgreSQL: estado healthy
Alembic: migración inicial aplicada
Swagger: accesible
```

## Pruebas implementadas

La suite incluye:

- pruebas unitarias de servicios con repositorios falsos;
- pruebas de repositorios con SQLite temporal;
- pruebas HTTP mediante `TestClient`;
- pruebas de integración con routers, servicios, repositorios, modelos y SQLite reales.

Las bases temporales evitan modificar `sensorhub.db` durante las pruebas.

## Seguridad de configuración

Los valores locales de PostgreSQL se almacenan en:

```text
.env
```

Este archivo se encuentra excluido mediante `.gitignore`.

El repositorio solo conserva:

```text
.env.example
```

con valores de referencia que deben sustituirse localmente.

No deben almacenarse contraseñas reales en:

- el código fuente;
- `docker-compose.yml`;
- `README.md`;
- `AI_LOG.md`;
- el historial de Git.

## Decisiones arquitectónicas

Las decisiones principales se documentan en:

```text
docs/adr/
```

Entre ellas se encuentran:

- persistencia mediante SQLAlchemy 2.x;
- uso local de SQLite;
- conexión configurable con PostgreSQL;
- arquitectura en capas;
- inyección de dependencias con FastAPI;
- separación entre modelos ORM y esquemas Pydantic;
- uso de Alembic para versionar el esquema.

## Historial del curso

Las carpetas semanales conservan los ejercicios anteriores:

- `semana1/`: principios SOLID y driver UART;
- `semana2/`: Scrum, historias de usuario y TDD;
- `app/`: producto SensorHub desarrollado a partir de la Semana 3.

El driver UART continúa disponible dentro del historial de la Semana 1, pero ya no representa el producto principal del repositorio.

## Uso de inteligencia artificial

El uso de herramientas de IA durante el desarrollo se encuentra documentado en:

```text
AI_LOG.md
```

La bitácora registra los prompts utilizados, las propuestas obtenidas, las decisiones tomadas, los cambios realizados y su justificación.