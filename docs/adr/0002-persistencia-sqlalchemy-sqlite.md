# ADR-0002: Persistencia con SQLAlchemy 2.x y SQLite

- Estado: Aceptado
- Fecha: 2026-07-28
- Actualizado: 2026-07-31
- Nota: el modelo de datos original fue ampliado durante el ejercicio integrador de SensorHub.

## Contexto

SensorHub necesita almacenar sensores y lecturas para que la información permanezca disponible después de cerrar la aplicación.

Mantener los datos únicamente en memoria provocaría su pérdida al finalizar el proceso. La solución debía ser tipada, comprobable mediante pruebas y suficientemente sencilla para el desarrollo local.

Durante la primera implementación solamente se almacenaban lecturas con temperatura y humedad. Posteriormente, SensorHub evolucionó para administrar sensores como entidades independientes y almacenar una sola magnitud por lectura.

## Decisión

Se utilizará SQLAlchemy 2.x como ORM y SQLite como base de datos inicial.

La implementación incluye:

- un `Engine` conectado a `sensorhub.db`;
- una clase declarativa `Base`;
- la fábrica de sesiones `SessionLocal`;
- modelos ORM tipados mediante `Mapped` y `mapped_column`;
- repositorios para administrar el acceso a datos;
- un procedimiento reproducible para crear las tablas;
- pruebas con bases SQLite temporales.

La inicialización del esquema se ejecuta mediante:

```bash
python -m app.init_db
```

## Evolución del modelo de datos

### Modelo inicial

La primera versión de la tabla `readings` contenía:

- `id`;
- `sensor_id`;
- `temperature`;
- `humidity`;
- `received_at`.

Esta estructura fue suficiente para practicar la configuración inicial de SQLAlchemy, las sesiones y la persistencia.

### Modelo actual

Durante el ejercicio integrador se creó una tabla independiente para sensores y se modificó el modelo de lecturas.

La tabla `sensors` contiene:

- `id` como clave primaria;
- `name`;
- `sensor_type`;
- `unit`;
- `is_active`.

La tabla `readings` contiene:

- `id` como clave primaria;
- `sensor_id`;
- `value`;
- `unit`;
- `received_at`.

Cada lectura representa una sola medición y se asocia con un sensor.

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

### SQLite

SQLite permite utilizar una base de datos real sin instalar o administrar un servidor externo.

Es apropiada para esta etapa porque:

- funciona mediante un archivo local;
- simplifica la instalación;
- permite crear bases temporales durante las pruebas;
- es suficiente para el volumen y concurrencia actuales;
- puede sustituirse posteriormente sin modificar los routers.

### Normalización

La tabla `sensors` almacena los metadatos que identifican a cada sensor.

La tabla `readings` almacena las mediciones relacionadas con esos sensores.

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

### PostgreSQL

Ofrece mayor capacidad para producción, concurrencia y despliegue, pero añade complejidad operativa innecesaria para esta etapa.

La arquitectura permite considerarlo posteriormente sin reescribir las capas HTTP y de negocio.

### Una sola tabla para sensores y lecturas

Se descartó al ampliar SensorHub porque duplicaría los metadatos del sensor y dificultaría administrar su nombre, tipo, unidad y estado.

## Consecuencias

### Positivas

- Persistencia real de sensores y lecturas.
- Modelos ORM tipados.
- Separación entre configuración, modelos, repositorios y servicios.
- Pruebas independientes mediante SQLite temporal.
- Sesiones controladas mediante inyección de dependencias.
- Posibilidad de sustituir SQLite por otra base de datos.
- Menor duplicación de metadatos de sensores.

### Negativas

- SQLite tiene limitaciones de concurrencia y escalabilidad.
- SQLite no conserva completamente la información de zona horaria en `DateTime`.
- El esquema todavía no utiliza migraciones versionadas.
- Los cambios estructurales requieren recrear manualmente la base local.
- La clave foránea está declarada, pero SQLite no la aplica automáticamente mientras no se active `PRAGMA foreign_keys`.
- La solución utiliza más archivos que una implementación directa con `sqlite3`.

## Resultado

SensorHub utiliza SQLAlchemy 2.x y SQLite para persistir sensores y lecturas mediante repositorios tipados.

La decisión inicial de utilizar SQLAlchemy y SQLite se conserva. Lo que cambió fue el modelo de datos: la tabla original de lecturas fue reemplazada por una estructura normalizada con sensores independientes y lecturas de una sola magnitud.

El funcionamiento fue comprobado mediante pruebas de repositorios, pruebas de integración con SQLite temporal y validación manual desde Swagger.