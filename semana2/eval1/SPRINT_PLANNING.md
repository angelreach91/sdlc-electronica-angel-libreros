# Planeación del Sprint 1

## Sprint Goal

Construir y verificar mediante TDD el núcleo del sistema de monitoreo ambiental de la bodega industrial, de manera que permita registrar sensores, recibir y validar lecturas de temperatura y humedad, detectar anomalías utilizando umbrales configurables y generar alertas que puedan mostrarse en consola y almacenarse en un archivo.

El incremento deberá cumplir las comprobaciones de calidad definidas para el proyecto: pruebas automatizadas, cobertura mínima del 80 %, Ruff y Mypy sin errores, aplicación comprensible de principios SOLID y evidencia del ciclo RED → GREEN → REFACTOR.

## Historias seleccionadas

| Historia | Descripción | MoSCoW | Story Points | Estado |
|---|---|---:|---:|---|
| US-01 | Registrar un sensor | Must | 3 | Done |
| US-02 | Registrar una lectura de temperatura y humedad | Must | 3 | Sprint |
| US-03 | Validar los datos de una lectura | Must | 3 | Sprint |
| US-04 | Configurar los umbrales de anomalía | Must | 3 | Sprint |
| US-05 | Detectar condiciones ambientales anómalas | Must | 5 | Sprint |
| US-06 | Generar una alerta para una lectura anómala | Must | 5 | Sprint |
| US-07 | Mostrar y guardar las alertas | Must | 5 | Sprint |

**Total seleccionado:** 7 historias y 27 Story Points.

## Justificación de la selección

Las historias `US-01` a `US-07` fueron seleccionadas porque conforman un flujo funcional completo para el núcleo del sistema.

La `US-01` permite identificar los sensores que producirán las mediciones. Las historias `US-02` y `US-03` permiten representar, registrar y validar las lecturas ambientales. Las historias `US-04` y `US-05` incorporan la configuración de los umbrales y la detección de condiciones anómalas. Finalmente, las historias `US-06` y `US-07` permiten generar las alertas y enviarlas mediante estrategias de consola y archivo.

El orden seleccionado respeta las dependencias entre funcionalidades:

1. Registrar el sensor.
2. Recibir su lectura.
3. Validar sus datos.
4. Proporcionar los umbrales.
5. Detectar las anomalías.
6. Construir una alerta.
7. Mostrarla y almacenarla.

La `US-01` ya fue completada durante el Sprint. Las historias `US-02` a `US-07` permanecen como trabajo pendiente. Las historias `US-08` a `US-12` continúan en el Product Backlog porque dependen del funcionamiento previo del núcleo y no son necesarias para obtener el primer incremento funcional.

## Descomposición en tareas

Todas las tareas tienen una duración estimada máxima de cuatro horas.

### US-01: Registrar un sensor — completada

- Diseñar pruebas para el registro, la consulta y el rechazo de identificadores inválidos — 1 hora.
- Implementar el registro de sensores — 1.5 horas.
- Refactorizar y ejecutar las comprobaciones de calidad — 0.5 horas.

### US-02: Registrar una lectura de temperatura y humedad

- Escribir las pruebas para una lectura válida y para un sensor inexistente — 1 hora.
- Implementar `SensorReading` y el registro de lecturas — 1.5 horas.
- Refactorizar y ejecutar las comprobaciones de calidad — 0.5 horas.

### US-03: Validar los datos de una lectura

- Escribir pruebas para valores válidos, incompletos, no numéricos y fuera de rango — 1 hora.
- Implementar las reglas de validación de las lecturas — 1 hora.
- Refactorizar el manejo de errores y comprobar los casos límite — 0.5 horas.

### US-04: Configurar los umbrales de anomalía

- Escribir pruebas para umbrales predeterminados, personalizados e inválidos — 1 hora.
- Implementar la configuración de los umbrales — 1 hora.
- Preparar la inyección de los umbrales en el detector — 0.5 horas.
- Refactorizar y ejecutar las comprobaciones de calidad — 0.5 horas.

### US-05: Detectar condiciones ambientales anómalas

- Escribir pruebas para anomalías de temperatura, humedad y ambas variables — 1 hora.
- Probar los casos límite donde los valores sean iguales a los umbrales — 0.5 horas.
- Implementar `AnomalyDetector` con umbrales inyectados — 1.5 horas.
- Refactorizar la representación del resultado — 0.5 horas.

### US-06: Generar una alerta para una lectura anómala

- Escribir pruebas para una alerta individual, una consolidada y una lectura normal — 1 hora.
- Implementar la representación de una alerta — 1 hora.
- Implementar `AlertManager` evitando alertas duplicadas — 1 hora.
- Refactorizar y ejecutar las comprobaciones de calidad — 0.5 horas.

### US-07: Mostrar y guardar las alertas

- Escribir pruebas para la estrategia de consola — 0.5 horas.
- Escribir pruebas para creación, conservación y fallo del archivo — 1 hora.
- Definir la abstracción para las estrategias de salida — 0.5 horas.
- Implementar la estrategia de consola — 1 hora.
- Implementar la estrategia de archivo JSON Lines — 1.5 horas.
- Refactorizar y ejecutar las comprobaciones de calidad — 0.5 horas.

## Definition of Done

La Definition of Done aplicable al Sprint se encuentra en `semana2/DEFINITION_OF_DONE.md`. Para considerar terminada una historia se comprobará que:

- Sus criterios Gherkin estén representados mediante pruebas automatizadas.
- Exista evidencia real del ciclo RED → GREEN → REFACTOR.
- Todas las pruebas estén aprobadas.
- La cobertura sea igual o superior al 80 %.
- Ruff termine sin errores.
- Mypy termine sin errores.
- El código tenga nombres claros y responsabilidades separadas.
- Las decisiones relevantes sobre el uso de IA estén documentadas.
- Los cambios hayan sido revisados mediante un Pull Request antes del merge.