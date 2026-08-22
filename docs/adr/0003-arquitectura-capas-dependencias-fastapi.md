# ADR-0003: Arquitectura en capas e inyección de dependencias para SensorHub

- Estado: Aceptado
- Fecha: 2026-07-30
- Actualizado: 2026-07-31
- Revisado: 2026-08-21

## Contexto

SensorHub comenzó como una aplicación sencilla de FastAPI con los esquemas y endpoints definidos directamente en `app/main.py`.

Posteriormente se incorporaron persistencia con SQLite, modelos ORM de SQLAlchemy, repositorios y servicios. Para conectar estos componentes con la API era necesario evitar que los routers administraran sesiones, ejecutaran consultas SQL o concentraran reglas de negocio. En el estado final, la misma separación admite PostgreSQL 16 y SQLite mediante la configuración de `DATABASE_URL`.

La aplicación también debía ofrecer operaciones CRUD para sensores y lecturas, paginación, filtros por fecha, validación física y documentación automática mediante Swagger. Después se incorporaron alertas, estadísticas por sensor, observabilidad, configuración por entorno y manejo global de errores sin abandonar la arquitectura elegida.

## Decisión

Se utilizará una arquitectura en capas cuyo flujo de dependencias principal es:

```text
Router
  ↓
Service
  ↓
Repository Protocol
  ↓
SQLAlchemy Repository
  ↓
Model
  ↓
Database (PostgreSQL o SQLite)
```

Las capas se conectan mediante inyección de dependencias.

La estructura principal es:

```text
app/
├── main.py
├── config.py
├── db.py
├── dependencies.py
├── observability.py
├── sensor_types.py
├── models/
├── repositories/
├── services/
├── schemas/
└── routers/
```

## Responsabilidades de cada capa

### Routers

Los routers representan la capa de presentación HTTP.

Sus responsabilidades son:

- recibir parámetros de ruta, consulta y cuerpos JSON;
- delegar las operaciones en los servicios;
- devolver los códigos de estado correspondientes;
- utilizar esquemas Pydantic para documentar entradas y salidas.

Los errores compartidos no se traducen principalmente mediante bloques `try/except` repetidos. Los exception handlers globales convierten `ValueError`, `LookupError`, `SensorAlreadyExistsError`, `SQLAlchemyError` y excepciones inesperadas en respuestas HTTP consistentes. Un router puede conservar una decisión HTTP local, por ejemplo devolver `404` cuando un servicio retorna `None`.

Los routers no realizan consultas SQL ni contienen las reglas físicas del sistema.

Las rutas se encuentran separadas en:

- `app/routers/sensors.py`;
- `app/routers/readings.py`;
- `app/routers/alerts.py`.

### Services

Los servicios contienen las reglas de negocio y coordinan las operaciones.

`SensorService` se encarga de:

- normalizar identificadores y nombres;
- evitar sensores duplicados;
- validar la compatibilidad entre tipo y unidad;
- administrar actualizaciones parciales;
- desactivar sensores;
- validar la paginación.

`ReadingService` se encarga de:

- comprobar que el sensor exista;
- comprobar que el sensor esté activo;
- validar la unidad correspondiente al tipo de sensor;
- rechazar temperaturas inferiores a `-273.15 °C`;
- validar humedades entre `0 %` y `100 %`;
- coordinar la creación, consulta, actualización y eliminación;
- validar la paginación y los rangos de fechas;
- solicitar estadísticas por sensor y período sin cargar todas las lecturas en Python.

`AnomalyService` evalúa cada lectura almacenada y genera una alerta cuando `value > threshold`; además delega la notificación en una estrategia intercambiable.

`AlertService` se encarga de consultar alertas, validar filtros y paginación, listar alertas activas y aplicar únicamente las transiciones `open -> acknowledged` y `acknowledged -> resolved`.

Los servicios no dependen de FastAPI ni ejecutan consultas SQL directamente.

### Repositories

Los repositorios representan la capa de acceso a datos.

Sus responsabilidades son:

- recibir una sesión de SQLAlchemy;
- construir consultas mediante `select()`;
- agregar, consultar, actualizar y eliminar registros;
- aplicar paginación y filtros;
- ejecutar `commit()`, `refresh()` y `rollback()` cuando corresponde.

Los contratos de repositorio se definen mediante `Protocol`, incluidos `SensorRepository`, `SensorLookupRepository`, `ReadingRepository`, `AlertRepository` y los contratos mínimos consumidos por los servicios.

Las implementaciones utilizadas por la aplicación son:

- `SQLAlchemySensorRepository`;
- `SQLAlchemyReadingRepository`;
- `SQLAlchemyAlertRepository`.

Las estadísticas `MIN`, `MAX` y `AVG` se calculan en `SQLAlchemyReadingRepository` mediante agregaciones SQL.

Los repositorios no contienen reglas físicas ni producen respuestas HTTP.

### Models

Los modelos ORM representan las tablas de PostgreSQL o SQLite mediante la API tipada de SQLAlchemy 2.x.

La tabla `sensors` almacena:

- `id`;
- `name`;
- `location`;
- `sensor_type`;
- `unit`;
- `threshold`;
- `is_active`.

La tabla `readings` almacena:

- `id`;
- `sensor_id`;
- `value`;
- `unit`;
- `received_at`.

`readings.sensor_id` declara una clave foránea hacia `sensors.id`.

La tabla `alerts` almacena la lectura que originó la alerta, el valor, el umbral, la fecha de creación y su `status`.

### Schemas

Los esquemas Pydantic representan los contratos de entrada y salida de la API.

Se mantienen separados de los modelos ORM para evitar que la estructura HTTP dependa directamente de la implementación de persistencia.

Los esquemas se encuentran en:

- `app/schemas/sensor.py`;
- `app/schemas/reading.py`;
- `app/schemas/alert.py`.

## Inyección de dependencias

`app/dependencies.py` administra la construcción de las dependencias utilizadas por FastAPI.

El flujo general es:

```text
get_session()
    ↓
repositorio SQLAlchemy
    ↓
servicio
    ↓
router
```

`get_session()` proporciona una sesión durante la petición y la cierra al finalizar.

`get_sensor_service()` construye:

```text
Session
→ SQLAlchemySensorRepository
→ SensorService
```

`get_reading_service()` construye:

```text
Session
→ SQLAlchemyReadingRepository
→ SQLAlchemySensorRepository
→ SQLAlchemyAlertRepository
→ AnomalyService
→ ReadingService
```

`get_alert_service()` construye:

```text
Session
→ SQLAlchemyAlertRepository
→ AlertService
```

Esta estructura permite que los routers reciban servicios ya construidos sin conocer cómo se crea la sesión o qué repositorio concreto se utiliza.

## Flujo de una solicitud

El registro de una lectura sigue este recorrido:

```text
Cliente HTTP
→ Router de lecturas
→ Esquema Pydantic
→ ReadingService
→ Repository Protocols
→ Repositorios SQLAlchemy
→ Modelos SQLAlchemy
→ PostgreSQL o SQLite
→ Esquema de respuesta
→ Cliente HTTP
```

Ejemplo:

```text
POST /sensors/TEMP-01/readings
```

1. FastAPI recibe y valida el cuerpo JSON.
2. El router obtiene `ReadingService` mediante `Depends`.
3. El servicio consulta el sensor.
4. El servicio comprueba que exista y esté activo.
5. El servicio valida la unidad y el rango físico.
6. El repositorio almacena la lectura.
7. SQLAlchemy confirma la transacción.
8. FastAPI serializa el modelo mediante `ReadingResponse`.
9. La API responde con `201 Created`.

## Pruebas

La arquitectura permite utilizar diferentes tipos de prueba:

- pruebas unitarias de servicios con repositorios falsos;
- pruebas de repositorios con SQLite temporal;
- pruebas HTTP con dependencias sustituidas;
- pruebas de integración con todas las capas reales y SQLite temporal.

Los servicios se prueban sin FastAPI ni SQLite mediante implementaciones falsas que registran las llamadas realizadas a los repositorios.

Las pruebas de integración sustituyen únicamente `get_session`, por lo que utilizan routers, servicios, repositorios, modelos y SQLite reales.

## Configuración, observabilidad y errores

`app/config.py` obtiene mediante variables de entorno el nombre, la versión y el nivel de logging de la aplicación. `app/db.py` obtiene `DATABASE_URL` y normaliza las URL de PostgreSQL para utilizar el driver configurado.

`app/observability.py` aporta:

- middleware para registrar solicitudes y errores;
- `MetricsCollector` para `requests_total`, `errors_total` y `uptime_seconds`;
- logging JSON estructurado.

`app/main.py` conecta el middleware, expone `GET /health` y `GET /metrics`, e instala handlers globales con estas traducciones:

- `ValueError` → `400`;
- `LookupError` → `404`;
- `SensorAlreadyExistsError` → `409`;
- `SQLAlchemyError` → `503`;
- `Exception` → `500`.

## Alternativas consideradas

### Consultas SQL dentro de los routers

Se descartó porque mezcla presentación, reglas de negocio y persistencia, además de dificultar las pruebas.

### Crear las sesiones dentro de los repositorios

Se descartó porque ocultaría el ciclo de vida de la sesión y complicaría su sustitución durante las pruebas.

### Utilizar implementaciones concretas en los servicios

Se descartó para evitar que los servicios dependieran directamente de SQLAlchemy y para permitir repositorios falsos durante las pruebas.

### Concentrar toda la API en `app/main.py`

Fue adecuado para la primera versión, pero dejó de ser conveniente al crecer el número de endpoints y responsabilidades.

## Consecuencias

### Positivas

- Separación clara de responsabilidades.
- Menor acoplamiento entre FastAPI y SQLAlchemy.
- Servicios verificables sin base de datos.
- Repositorios verificables con SQLite temporal.
- Sustitución sencilla de dependencias durante las pruebas.
- Routers enfocados únicamente en HTTP.
- Posibilidad de cambiar la persistencia sin reescribir los routers.
- Swagger generado automáticamente a partir de los esquemas y rutas.

### Negativas

- La solución utiliza más archivos y clases que una aplicación monolítica pequeña.
- Es necesario mantener contratos consistentes entre servicios y repositorios.
- Algunos cambios requieren actualizar varias capas.
- Los contratos entre capas, la configuración y los handlers globales requieren mantenerse coordinados al incorporar nuevos casos de negocio.

## Resultado

La arquitectura permite administrar sensores, lecturas y alertas, además de consultar estadísticas y métricas, sin mezclar las reglas del dominio con FastAPI o SQLAlchemy.

La decisión de capas se conserva en el estado final: los servicios dependen de Repository Protocols, las implementaciones SQLAlchemy encapsulan PostgreSQL o SQLite y FastAPI compone las dependencias. El manejo global de errores y la observabilidad son responsabilidades transversales conectadas en la aplicación, no lógica repetida dentro de cada router.

El flujo completo fue verificado mediante pruebas automatizadas, SQLite temporal, PostgreSQL 16 y validaciones manuales de la API desplegada.
