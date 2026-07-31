# SensorHub

SensorHub es una API REST desarrollada con FastAPI para administrar sensores y sus lecturas.

El proyecto utiliza una arquitectura en cuatro capas, persistencia con SQLAlchemy 2.x y SQLite, validación mediante Pydantic, documentación automática con Swagger y pruebas automatizadas con Pytest.

Este repositorio también conserva los ejercicios realizados durante las semanas anteriores del curso como material histórico.

## Funcionalidades

SensorHub permite:

- registrar sensores de temperatura y humedad;
- consultar sensores existentes;
- actualizar parcialmente sus datos;
- desactivar sensores sin eliminarlos físicamente;
- registrar lecturas asociadas a un sensor;
- consultar lecturas mediante identificador;
- listar lecturas con paginación;
- filtrar lecturas por rango de fechas;
- actualizar lecturas;
- eliminar lecturas;
- rechazar datos que no respeten las reglas físicas definidas.

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

La aplicación sigue este flujo:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Model
  ↓
SQLite
```

### Routers

Reciben solicitudes HTTP, delegan las operaciones y generan las respuestas correspondientes.

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

Representan las tablas de SQLite mediante la API tipada de SQLAlchemy 2.x.

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
├── init_db.py
├── sensor_types.py
├── models/
├── repositories/
├── routers/
├── schemas/
└── services/

tests/
docs/adr/
semana1/
semana2/
AI_LOG.md
requirements.txt
pyproject.toml
```

## Instalación

Desde la raíz del repositorio:

```bash
python -m venv .venv
```

En Linux o WSL:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Inicialización de la base de datos

Crea las tablas de SQLite con:

```bash
python -m app.init_db
```

La aplicación utiliza por defecto:

```text
sensorhub.db
```

Este archivo es local y no se registra en Git.

## Ejecución de la API

Desde la raíz del repositorio y con el entorno virtual activado:

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
→ SQLite
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
ruff check app tests
```

Comprueba el tipado:

```bash
mypy app tests
```

Estado verificado al cierre del desarrollo del viernes:

```text
58 pruebas aprobadas
Cobertura total: 88.12 %
Ruff: sin errores
Mypy: sin errores
Swagger: validado manualmente
```

## Pruebas implementadas

La suite incluye:

- pruebas unitarias de servicios con repositorios falsos;
- pruebas de repositorios con SQLite temporal;
- pruebas HTTP mediante `TestClient`;
- pruebas de integración con routers, servicios, repositorios, modelos y SQLite reales.

Las bases temporales evitan modificar `sensorhub.db` durante las pruebas.

## Decisiones arquitectónicas

Las decisiones principales se documentan en:

```text
docs/adr/
```

Entre ellas se encuentran:

- persistencia mediante SQLAlchemy 2.x y SQLite;
- arquitectura en capas;
- inyección de dependencias con FastAPI;
- separación entre modelos ORM y esquemas Pydantic.

## Historial del curso

Las carpetas semanales conservan los ejercicios anteriores:

- `semana1/`: principios SOLID y driver UART;
- `semana2/`: Scrum, historias de usuario y TDD;
- `app/`: producto SensorHub desarrollado durante la Semana 3.

El driver UART sigue disponible dentro del historial de la Semana 1, pero ya no representa el producto principal del repositorio.

## Uso de inteligencia artificial

El uso de herramientas de IA durante el desarrollo se encuentra documentado en:

```text
AI_LOG.md
```

La bitácora registra los prompts utilizados, las propuestas obtenidas, las decisiones tomadas, los cambios realizados y su justificación.