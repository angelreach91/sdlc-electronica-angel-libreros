# ADR-0002: Persistencia con SQLAlchemy 2.x y SQLite

- Estado: Aceptado
- Fecha: 2026-07-28
- Actualizado: 2026-07-31
- Revisado: 2026-08-21
- Nota: el modelo de datos original fue ampliado durante el ejercicio integrador de SensorHub.

## Contexto

SensorHub necesita almacenar sensores y lecturas para que la información permanezca disponible después de cerrar la aplicación.

Mantener los datos únicamente en memoria provocaría su pérdida al finalizar el proceso. La solución debía ser tipada, comprobable mediante pruebas y suficientemente sencilla para el desarrollo local.

Durante la primera implementación solamente se almacenaban lecturas con temperatura y humedad. Posteriormente, SensorHub evolucionó para administrar sensores como entidades independientes y almacenar una sola magnitud por lectura.

## Decisión

La decisión inicial fue utilizar SQLAlchemy 2.x como ORM y SQLite como base de datos.

La implementación incluye:

- un `Engine` conectado a `sensorhub.db`;
- una clase declarativa `Base`;
- la fábrica de sesiones `SessionLocal`;
- modelos ORM tipados mediante `Mapped` y `mapped_column`;
- repositorios para administrar el acceso a datos;
- un procedimiento reproducible para crear las tablas;
- pruebas con bases SQLite temporales.

En esa etapa, la inicialización del esquema se ejecutaba mediante:

```bash
python -m app.init_db
```

## Revisión final — 2026-08-21

SQLAlchemy 2.x se conserva como capa de persistencia. La evolución del proyecto no sustituyó el ORM ni el patrón repositorio; amplió los motores y el proceso de administración del esquema:

- SQLite continúa disponible como fallback local y como base de datos para pruebas automatizadas;
- PostgreSQL 16 es la persistencia utilizada por Docker Compose y por el despliegue de producción en Render;
- `DATABASE_URL` selecciona y configura la conexión sin modificar routers ni servicios;
- Alembic administra las migraciones versionadas;
- la cadena de migraciones tiene un único head: `b7f2c8d91e34`.

Por tanto, SQLite describe la decisión inicial y sigue siendo una opción soportada, pero ya no es la única persistencia actual. Los cambios de esquema se aplican mediante Alembic, incluida la preparación de una base vacía hasta `upgrade head`.

## Evolución del modelo de datos

### Modelo inicial

La primera versión de la tabla `readings` contenía:

- `id`;
- `sensor_id`;
- `temperature`;
- `humidity`;
- `received_at`.

Esta estructura fue suficiente para practicar la configuración inicial de SQLAlchemy, las sesiones y la persistencia.

### Modelo final

Durante el ejercicio integrador se creó una tabla independiente para sensores y se modificó el modelo de lecturas.

La tabla `sensors` contiene:

- `id` como clave primaria;
- `name`;
- `location`;
- `sensor_type`;
- `unit`;
- `threshold`;
- `is_active`.

La tabla `readings` contiene:

- `id` como clave primaria;
- `sensor_id`;
- `value`;
- `unit`;
- `received_at`.

Cada lectura representa una sola medición y se asocia con un sensor.

La tabla `alerts` contiene:

- `id` como clave primaria;
- `sensor_id`;
- `reading_id`;
- `value`;
- `threshold`;
- `status`;
- `created_at`.

`status` conserva los estados `open`, `acknowledged` y `resolved` definidos para el ciclo de vida de las alertas.

El modelo ORM declara la relación:

```text
readings.sensor_id → sensors.id
```

La restricción está definida en SQLAlchemy y aparece en el esquema de SQLite. Sin embargo, la configuración actual del motor no activa explícitamente `PRAGMA foreign_keys=ON`.

Por ello, la API protege la creación de lecturas huérfanas mediante `ReadingService`, que comprueba que el sensor exista antes de delegar la persistencia.

## Fundamentos de la decisión

### SQLAlchemy 2.x

SQLAlchemy permite trabajar con modelos y consultas mediante una API tipada.

La implementación utiliza:

- `DeclarativeBase`;
- `Mapped[...]`;
- `mapped_column`;
- `select`;
- `Session`;
- `commit`;
- `refresh`;
- `rollback`.

Esto mantiene la persistencia separada de las reglas de negocio y evita escribir consultas SQL directamente dentro de los routers.

### SQLite y PostgreSQL

SQLite permitió utilizar inicialmente una base de datos real sin instalar o administrar un servidor externo y continúa siendo útil como fallback local y para pruebas.

Es apropiada para desarrollo local y pruebas porque:

- funciona mediante un archivo local;
- simplifica la instalación;
- permite ejecutar pruebas aisladas con bases temporales.

La separación provista por SQLAlchemy y los repositorios permitió incorporar PostgreSQL 16 sin modificar las capas HTTP y de negocio. PostgreSQL es ahora el motor utilizado en Docker Compose y producción.

### Normalización

La tabla `sensors` almacena los metadatos que identifican a cada sensor, incluida su ubicación y el umbral opcional para generar alertas.

La tabla `readings` almacena las mediciones relacionadas con esos sensores.

La tabla `alerts` almacena los eventos generados cuando una lectura supera el umbral del sensor y conserva su estado de atención.

Separar ambas entidades evita repetir en cada lectura:

- el nombre del sensor;
- su tipo;
- su unidad principal;
- su estado activo.

Cada fila de `readings` representa una sola medición atómica mediante `value` y `unit`.

### Transacciones

Los repositorios administran las operaciones de persistencia mediante sesiones de SQLAlchemy.

En las operaciones de escritura se utilizan:

```text
session.add()
session.commit()
session.refresh()
```

Si una operación falla durante la transacción, se ejecuta:

```text
session.rollback()
```

Las pruebas de repositorio abren nuevas sesiones después de crear o actualizar registros para demostrar que la información fue persistida realmente y no permaneció únicamente en el objeto de la sesión inicial.

## Pruebas

Las pruebas de persistencia utilizan bases SQLite temporales creadas mediante `tmp_path`.

Esto permite comprobar:

- creación y recuperación de sensores;
- actualización persistida entre sesiones;
- creación y recuperación de lecturas;
- actualización y eliminación de lecturas;
- paginación;
- filtrado por sensor;
- filtros por rango de fechas;
- orden estable de los resultados.

Las pruebas temporales no modifican `sensorhub.db`.

## Alternativas consideradas

### Módulo `sqlite3`

Permitiría trabajar directamente con SQLite, pero exigiría escribir consultas SQL, conversiones y manejo de filas manualmente.

Se descartó porque el objetivo de la semana incluye utilizar SQLAlchemy 2.x y el patrón repositorio.

### Almacenamiento en memoria

Es sencillo y útil para algunos dobles de prueba, pero los datos se perderían al detener la aplicación.

No es adecuado como persistencia principal.

### PostgreSQL — evaluación inicial y evolución

En la decisión inicial, PostgreSQL ofrecía mayor capacidad para producción, concurrencia y despliegue, pero añadía complejidad operativa innecesaria para esa etapa.

La evolución final confirmó la sustituibilidad prevista: PostgreSQL 16 se incorporó mediante `DATABASE_URL` y se utiliza en Docker Compose y Render sin reescribir las capas HTTP y de negocio.

### Una sola tabla para sensores y lecturas

Se descartó al ampliar SensorHub porque duplicaría los metadatos del sensor y dificultaría administrar su nombre, tipo, unidad y estado.

## Consecuencias

### Positivas

- Persistencia real de sensores, lecturas y alertas.
- Modelos ORM tipados.
- Separación entre configuración, modelos, repositorios y servicios.
- Pruebas independientes mediante SQLite temporal.
- Sesiones controladas mediante inyección de dependencias.
- Posibilidad de sustituir SQLite por otra base de datos.
- Uso de PostgreSQL 16 en los entornos que requieren un servidor de base de datos.
- Evolución reproducible del esquema mediante migraciones de Alembic.
- Menor duplicación de metadatos de sensores.

### Negativas

- El fallback SQLite mantiene limitaciones de concurrencia, escalabilidad y conservación de zona horaria en `DateTime`.
- La operación con PostgreSQL añade un servicio externo y configuración mediante variables de entorno.
- Los cambios estructurales deben mantenerse coordinados con las migraciones versionadas de Alembic.
- La clave foránea está declarada, pero SQLite no la aplica automáticamente mientras no se active `PRAGMA foreign_keys`.
- La solución utiliza más archivos que una implementación directa con `sqlite3`.

## Resultado

SensorHub utiliza SQLAlchemy 2.x y repositorios tipados para persistir sensores, lecturas y alertas.

La decisión inicial de utilizar SQLAlchemy y SQLite se conserva como origen de la arquitectura de persistencia. El estado final mantiene SQLite como fallback local y base para pruebas, utiliza PostgreSQL 16 con Docker Compose y en producción, y administra el esquema con Alembic.

Además, el modelo evolucionó desde la tabla original de lecturas hasta una estructura normalizada con sensores —incluidos `location` y `threshold`—, lecturas de una sola magnitud y alertas con `status`.

El funcionamiento fue comprobado mediante pruebas de repositorios e integración, una base vacía migrada hasta el único head y validaciones con SQLite y PostgreSQL.
