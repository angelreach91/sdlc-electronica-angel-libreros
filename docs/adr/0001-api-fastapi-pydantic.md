# ADR-0001: Uso de FastAPI y Pydantic para la API de SensorHub

- Estado: Aceptado
- Fecha: 2026-07-27

## Contexto

SensorHub necesita exponer operaciones HTTP para comprobar el estado del servicio y recibir lecturas de sensores. La API debe validar los datos de entrada, utilizar tipos explícitos y generar respuestas coherentes.

## Decisión

Se utilizará FastAPI como framework para construir la API REST y Pydantic para definir y validar los modelos de entrada y salida.

La implementación inicial incluye:

- `GET /health` para comprobar el estado del servicio.
- `POST /readings` para recibir lecturas.
- `ReadingInput` como modelo de entrada.
- `ReadingResponse` como modelo de respuesta.
- Validación de `sensor_id`, temperatura y humedad.
- Respuesta `201 Created` para lecturas aceptadas.
- Respuesta `422 Unprocessable Entity` para datos inválidos.

## Alternativas consideradas

### Flask

Es una alternativa ligera, pero requiere configurar manualmente una mayor parte de la validación, el tipado y la documentación OpenAPI.

### Django REST Framework

Proporciona muchas herramientas, pero resulta más complejo de lo necesario para el alcance actual de SensorHub.

## Consecuencias

### Positivas

- Validación automática de las solicitudes.
- Documentación OpenAPI generada automáticamente.
- Uso de modelos tipados.
- Integración sencilla con pruebas automatizadas.
- Respuestas HTTP consistentes.

### Negativas

- Se agregan FastAPI, Pydantic y Uvicorn como dependencias.
- Los modelos de la API deberán mantenerse coordinados con el dominio y la persistencia.
- En esta etapa, `POST /readings` todavía no almacena permanentemente la información.