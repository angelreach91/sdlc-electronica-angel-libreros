# ADR-0002: Persistencia con SQLAlchemy 2.x y SQLite

- Estado: Aceptado
- Fecha: 2026-07-28

## Contexto

SensorHub necesita almacenar las lecturas recibidas para recuperarlas posteriormente. Mantenerlas únicamente en memoria provocaría la pérdida de información al finalizar el proceso.

La solución debe ser tipada, comprobable mediante pruebas y suficientemente sencilla para el desarrollo local.

## Decisión

Se utilizará SQLAlchemy 2.x como ORM y SQLite como base de datos inicial.

La implementación incluye:

- Un `Engine` conectado a `sensorhub.db`.
- Una clase declarativa `Base`.
- La fábrica de sesiones `SessionLocal`.
- El modelo ORM `Reading`.
- Un procedimiento reproducible para crear las tablas.
- Una prueba de inserción y recuperación con una base temporal.

La tabla `readings` contiene:

- `id` como clave primaria.
- `sensor_id` como identificador indexado.
- `temperature`.
- `humidity`.
- `received_at`.

## Fundamentos de la decisión

### Normalización

Los valores almacenados son atómicos y cada fila representa una sola lectura. La clave primaria `id` identifica cada registro y los demás atributos dependen directamente de ella.

Para el alcance actual no se creó una tabla independiente de sensores, porque todavía no se almacenan metadatos adicionales sobre ellos. Si esa información se incorpora posteriormente, deberá separarse para evitar duplicación.

### Índice de `sensor_id`

Se agregó un índice a `sensor_id` porque será frecuente consultar las lecturas pertenecientes a un sensor específico.

El índice acelera estas búsquedas, aunque utiliza espacio adicional y añade un pequeño costo durante las inserciones y actualizaciones.

### Transacciones ACID

Las sesiones de SQLAlchemy y las transacciones de SQLite proporcionan:

- Atomicidad: el `commit` confirma la operación completa.
- Consistencia: la transacción conserva las restricciones definidas por el modelo.
- Aislamiento: las transacciones evitan interferencias incorrectas entre operaciones.
- Durabilidad: después del `commit`, la lectura permanece almacenada incluso cuando se cierra la sesión.

## Alternativas consideradas

### Módulo `sqlite3`

Permitiría trabajar directamente con SQLite, pero exigiría escribir consultas SQL y conversiones manuales.

### Almacenamiento en memoria

Es sencillo, pero los datos se perderían al detener la aplicación.

### PostgreSQL

Ofrece mayor capacidad para producción y concurrencia, pero añade complejidad operativa innecesaria para esta etapa.

## Consecuencias

### Positivas

- Persistencia real de las lecturas.
- Modelos ORM tipados.
- Separación entre la configuración y los modelos.
- Sesiones reutilizables para las futuras capas del sistema.
- Pruebas independientes mediante SQLite temporal.

### Negativas

- SQLite tiene limitaciones de concurrencia y escalabilidad.
- SQLite no conserva completamente la zona horaria del tipo `datetime`.
- La creación del esquema todavía no utiliza migraciones versionadas.
- Será necesario integrar la persistencia con los endpoints posteriormente.