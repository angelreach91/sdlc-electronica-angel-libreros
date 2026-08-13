# AI Code Review — Semana 5

## Objetivo

Realizar una revisión crítica asistida por IA sobre `ReadingService`, evaluando posibles violaciones de SOLID, casos borde, riesgos de seguridad, problemas de rendimiento y validaciones incompletas.

La revisión fue realizada con Codex. Las sugerencias de la IA no se implementaron automáticamente: cada hallazgo fue evaluado antes de decidir si debía aceptarse, rechazarse o comprobarse mediante pruebas.

## Archivo revisado

`app/services/reading_service.py`

También se consultaron posteriormente los schemas, router y pruebas relacionadas con lecturas para identificar casos borde todavía no cubiertos.

---

## Primera revisión con Codex

Codex identificó nueve posibles hallazgos.

| ID | Hallazgo | Evaluación | Decisión |
|---|---|---|---|
| CR-01 | Valores `NaN` e infinitos podían superar la validación de temperatura | El servicio solo comprobaba el límite mínimo de temperatura. `NaN` y `+inf` no cumplían la condición de rechazo y podían continuar hacia persistencia. | Aceptado |
| CR-02 | Manejo inconsistente de datetimes con y sin zona horaria | Mezclar un datetime naive con uno timezone-aware podía producir `TypeError` durante la comparación. | Aceptado |
| CR-03 | Comprobación del sensor e inserción no atómicas | Es un riesgo posible de concurrencia, pero corregirlo requeriría introducir una unidad de trabajo o cambios transaccionales fuera del alcance de esta revisión. | Rechazado para el alcance actual |
| CR-04 | PATCH no distinguía campo omitido de `null` explícito | `ReadingUpdate` permitía `None`, por lo que un `null` enviado por el cliente podía interpretarse igual que un campo omitido. | Aceptado |
| CR-05 | `offset` no tiene límite superior | SensorHub no define actualmente un máximo para `offset`. Agregar uno sería introducir un requisito arbitrario. | Rechazado |
| CR-06 | Existían dos fuentes de verdad para la unidad del sensor | La consistencia entre tipo y unidad ya se valida durante el flujo normal de creación del sensor. El problema dependería de datos corruptos o modificaciones externas. | Rechazado para el alcance actual |
| CR-07 | Se consulta el sensor antes de validar argumentos simples | El impacto es pequeño y cambiar el orden también modificaría qué error tiene prioridad. | Rechazado |
| CR-08 | Las anotaciones numéricas no validan tipos en runtime | La frontera HTTP ya aplica validación mediante FastAPI/Pydantic y el proyecto utiliza type hints y mypy internamente. | Rechazado |
| CR-09 | `ReadingService` dependía de una interfaz más amplia de la necesaria | El servicio solo necesita `get_by_id()` pero dependía de un protocolo con varias operaciones de sensores. | Aceptado |

La revisión también concluyó que no existía una violación clara de SRP y que la inversión de dependencias ya estaba razonablemente aplicada.

No se identificaron construcciones dinámicas de SQL ni un riesgo directo de inyección dentro de `ReadingService`.

---

## Segunda revisión: casos borde

Se pidió a Codex identificar casos borde todavía ausentes en las pruebas existentes, sin modificar código ni inventar nuevos requisitos.

A partir de sus propuestas se seleccionaron ocho pruebas con valor real para SensorHub:

1. Rechazar temperatura `NaN`.
2. Rechazar temperatura `+Infinity`.
3. Rechazar de forma controlada un rango que mezcle datetime naive y timezone-aware.
4. Rechazar `value: null` explícito en PATCH.
5. Rechazar `unit: null` explícito en PATCH.
6. Aceptar exactamente `-273.15 °C`.
7. Aceptar exactamente `0 %` de humedad.
8. Aceptar exactamente `100 %` de humedad.

No se incorporaron propuestas sobre límites máximos de temperatura, offsets arbitrarios, rangos máximos de fechas o IDs excesivamente largos porque SensorHub no define esas reglas.

---

## Evidencia RED

Después de agregar las nuevas pruebas sin modificar producción se ejecutó:

```bash
python -m pytest tests/test_reading_service.py tests/test_readings_api.py -q
```

Resultado relevante:

```text
5 failed, 31 passed
```

Los cinco fallos revelaron comportamientos reales:

### 1. Temperatura NaN

`ReadingService` no generó el `ValueError` esperado.

### 2. Temperatura +Infinity

`ReadingService` tampoco rechazó el valor infinito positivo.

### 3. Datetimes incompatibles

Al mezclar una fecha sin zona horaria con otra timezone-aware se obtuvo:

```text
TypeError: can't compare offset-naive and offset-aware datetimes
```

### 4. PATCH con `value: null`

La API respondió `200 OK` cuando la prueba esperaba `422`.

### 5. PATCH con `unit: null`

La API respondió igualmente `200 OK` en lugar de `422`.

Los tres casos de límites físicos exactos ya funcionaban correctamente y no generaron fallos.

---

## Correcciones implementadas

### Valores no finitos

Se agregó una validación con `math.isfinite()` en `ReadingService`.

Cualquier medición `NaN`, `+Infinity` o `-Infinity` es rechazada antes de aplicar las reglas específicas del tipo de sensor.

### Datetimes con distinta conciencia de zona horaria

Antes de comparar `from_date` y `to_date`, el servicio comprueba si ambos poseen el mismo tipo de conciencia de zona horaria.

Una combinación naive/aware genera ahora un `ValueError` controlado en lugar de un `TypeError`.

No se prohibieron todos los datetimes naive ni se introdujo una nueva política temporal.

### `null` explícito en PATCH

`ReadingUpdate` incorporó un `field_validator` de Pydantic.

Los campos siguen siendo opcionales para permitir un PATCH parcial, pero si `value` o `unit` aparecen explícitamente con valor `null`, la entrada es rechazada por validación y la API responde `422`.

---

## Refactor ISP

Se aceptó también el hallazgo CR-09.

Se creó el protocolo:

```python
class SensorLookupRepository(Protocol):
    def get_by_id(self, sensor_id: str) -> Sensor | None:
        ...
```

`ReadingService` depende ahora de `SensorLookupRepository` en lugar del contrato completo `SensorRepository`.

`SQLAlchemySensorRepository` continúa funcionando mediante structural typing y no fue necesario modificar su implementación.

`SensorRepository` se mantiene para los consumidores que sí necesitan las operaciones completas de sensores.

Este cambio reduce el acoplamiento y aplica mejor Interface Segregation Principle sin modificar comportamiento funcional.

---

## Evidencia GREEN

Después de las correcciones se ejecutaron nuevamente las pruebas específicas:

```bash
python -m pytest tests/test_reading_service.py tests/test_readings_api.py -q --no-cov
```

Resultado:

```text
36 passed
```

Esto confirmó que los cinco fallos detectados pasaron de RED a GREEN.

---

## Validación final

Se ejecutaron los mismos controles principales utilizados por el pipeline del proyecto.

### Ruff

```bash
python -m ruff check app tests migrations
```

Resultado: sin errores.

### Mypy

```bash
python -m mypy app
```

Resultado: sin errores.

### Suite completa

```bash
python -m pytest
```

Resultado:

```text
69 passed
```

Cobertura total:

```text
90.71 %
```

El requisito mínimo configurado es 80 %.

---

## Conclusión

La IA fue útil para detectar posibles defectos y proponer casos borde, pero sus recomendaciones no se trataron como instrucciones automáticas.

De nueve hallazgos iniciales se implementaron únicamente aquellos que podían justificarse mediante el comportamiento real del sistema, pruebas reproducibles o un principio de diseño aplicable al código existente.

También se rechazaron propuestas que implicaban introducir requisitos inexistentes, optimizaciones prematuras o cambios arquitectónicos desproporcionados.

El proceso utilizado fue:

```text
Auditoría con IA
→ evaluación humana
→ selección de casos borde
→ pruebas RED
→ corrección mínima
→ pruebas GREEN
→ validación estática y suite completa
```

Esto permitió utilizar Codex como apoyo de code review manteniendo la decisión final y la responsabilidad técnica en la revisión humana.