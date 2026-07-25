# Backlog del sistema de monitoreo ambiental

## Reglas generales

- Cada lectura pertenece a un sensor registrado e incluye temperatura, humedad y fecha y hora de recepción.
- Una variable es anómala únicamente cuando supera su umbral vigente.
- Cada lectura puede producir como máximo una alerta; si ambas variables son anómalas, la alerta se mantiene consolidada.
- Los avisos de inactividad no se contabilizan como anomalías ambientales.
- Las consultas, los filtros, los resúmenes y las exportaciones no modifican el historial.

## Estado actual

El Product Backlog está ordenado de acuerdo con la prioridad MoSCoW y las dependencias funcionales del sistema. Las historias `US-01` a `US-07` fueron completadas durante el Sprint 1. Las historias `US-08` a `US-12` permanecen disponibles para Sprints posteriores.

| Orden | Historia | Prioridad | Story Points | Estado |
|---:|---|---|---:|---|
| 1 | US-01 — Registrar un sensor | Must | 3 | Done |
| 2 | US-02 — Registrar una lectura | Must | 3 | Done |
| 3 | US-03 — Validar una lectura | Must | 3 | Done |
| 4 | US-04 — Configurar umbrales | Must | 3 | Done |
| 5 | US-05 — Detectar anomalías | Must | 5 | Done |
| 6 | US-06 — Generar una alerta | Must | 5 | Done |
| 7 | US-07 — Mostrar y guardar alertas | Must | 5 | Done |
| 8 | US-08 — Consultar el historial | Should | 3 | Product Backlog |
| 9 | US-09 — Filtrar el historial | Should | 5 | Product Backlog |
| 10 | US-10 — Generar un resumen estadístico | Should | 5 | Product Backlog |
| 11 | US-11 — Detectar sensores inactivos | Should | 5 | Product Backlog |
| 12 | US-12 — Exportar un reporte | Could | 5 | Product Backlog |

**Total del Product Backlog:** 50 Story Points.  
**Completado en el Sprint 1:** 27 Story Points.  
**Trabajo pendiente:** 23 Story Points.

## Historias de usuario
## US-01: Registrar un sensor

**Como** operador de la bodega industrial,  
**quiero** registrar un sensor mediante un identificador único,  
**para** reconocer qué dispositivo produce cada lectura.

**Prioridad MoSCoW:** Must  
**Story points:** 3

### Escenario: Registrar un sensor nuevo

Given que no existe un sensor con el identificador "SENSOR-01"
When el operador registra el sensor con ese identificador
Then el sensor queda almacenado
And puede consultarse mediante "SENSOR-01"

### Escenario: Rechazar un identificador inválido

Given que el identificador está vacío o ya pertenece a otro sensor
When el operador intenta registrar el sensor
Then el sistema rechaza el registro
And informa la causa sin alterar los sensores existentes

## US-02: Registrar una lectura de temperatura y humedad

**Como** operador de la bodega industrial,  
**quiero** registrar las lecturas de temperatura y humedad de cada sensor,  
**para** conservar las condiciones ambientales medidas en la bodega.

**Prioridad MoSCoW:** Must  
**Story points:** 3

### Escenario: Registrar una lectura

Given que el sensor "SENSOR-01" está registrado
When el sistema recibe una lectura de temperatura y humedad
Then la asocia con "SENSOR-01"
And registra la fecha y hora de recepción
And conserva las lecturas registradas anteriormente

### Escenario: Recibir una lectura de un sensor inexistente

Given que el sensor "SENSOR-99" no está registrado
When el sistema recibe una lectura de ese sensor
Then rechaza la lectura
And informa que el sensor no existe

## US-03: Validar los datos de una lectura

**Como** operador de la bodega industrial,  
**quiero** que el sistema valide los datos de cada lectura,  
**para** evitar el registro de mediciones incompletas o inválidas.

**Prioridad MoSCoW:** Must  
**Story points:** 3

### Escenario: Aceptar una lectura válida

Given que el sensor está registrado
When el sistema recibe valores numéricos de temperatura y humedad
And la humedad se encuentra entre 0 % y 100 %
Then acepta la lectura
And permite continuar con su registro y análisis

### Escenario: Rechazar una lectura inválida

Given que el sensor está registrado
When la lectura está incompleta, contiene datos no numéricos o una humedad fuera de 0 % a 100 %
Then el sistema rechaza la lectura
And informa la causa
And no la almacena ni la analiza

## US-04: Configurar los umbrales de anomalía

**Como** responsable de la bodega industrial,  
**quiero** configurar los umbrales máximos de temperatura y humedad,  
**para** adaptar la detección de anomalías a las condiciones permitidas.

**Prioridad MoSCoW:** Must  
**Story points:** 3

### Escenario: Utilizar los umbrales predeterminados

Given que no existen umbrales personalizados
When el sistema inicia
Then utiliza 35 °C para temperatura
And utiliza 80 % para humedad

### Escenario: Configurar umbrales personalizados

Given que el responsable proporciona umbrales válidos
When guarda la configuración
Then los nuevos valores sustituyen a los anteriores
And se utilizan en los análisis posteriores

### Escenario: Rechazar una configuración inválida

Given que el sistema tiene umbrales vigentes
When el responsable proporciona un valor no numérico o una humedad fuera de 0 % a 100 %
Then el sistema rechaza la configuración
And conserva los umbrales anteriores

## US-05: Detectar condiciones ambientales anómalas

**Como** operador de la bodega industrial,  
**quiero** que cada lectura se compare con los umbrales vigentes,  
**para** identificar condiciones ambientales que requieren atención.

**Prioridad MoSCoW:** Must  
**Story points:** 5

### Escenario: Detectar una o ambas variables anómalas

Given que existe una lectura válida
When la temperatura, la humedad o ambas superan sus respectivos umbrales
Then el sistema identifica únicamente las variables que los superaron
And conserva sus valores y los umbrales utilizados

### Escenario: Procesar una lectura sin anomalías

Given que existe una lectura válida
When sus valores son menores o iguales a los umbrales vigentes
Then el sistema determina que no existen anomalías

## US-06: Generar una alerta para una lectura anómala

**Como** operador de la bodega industrial,  
**quiero** que el sistema genere una alerta por cada lectura anómala,  
**para** reconocer el sensor y las condiciones que requieren atención.

**Prioridad MoSCoW:** Must  
**Story points:** 5

### Escenario: Generar una alerta

Given que una lectura contiene una o más variables anómalas
When el sistema genera la alerta
Then crea una sola alerta para la lectura
And incluye el sensor, la fecha y hora, los valores anómalos y sus umbrales
And conserva juntas las anomalías cuando existen ambas

### Escenario: No generar una alerta

Given que una lectura no contiene variables anómalas
When el sistema procesa el resultado del análisis
Then no genera ninguna alerta

## US-07: Mostrar y guardar las alertas

**Como** operador de la bodega industrial,  
**quiero** visualizar y almacenar las alertas generadas,  
**para** atenderlas oportunamente y conservar un historial.

**Prioridad MoSCoW:** Must  
**Story points:** 5

### Escenario: Mostrar y guardar una alerta

Given que el sistema generó una alerta
And el archivo de alertas todavía no existe
When la procesa
Then muestra su información en la consola
And crea el archivo JSON Lines
And guarda un registro equivalente

### Escenario: Conservar las alertas anteriores

Given que el archivo ya contiene alertas
When el sistema guarda una nueva
Then conserva los registros anteriores
And agrega la alerta como un registro independiente

### Escenario: Fallar el almacenamiento

Given que existe una alerta y el archivo no puede escribirse
When el sistema procesa la alerta
Then todavía la muestra en la consola
And informa que no pudo almacenarla

## US-08: Consultar el historial de alertas

**Como** operador de la bodega industrial,  
**quiero** consultar las alertas almacenadas,  
**para** revisar las condiciones anómalas registradas anteriormente.

**Prioridad MoSCoW:** Should  
**Story points:** 3

### Escenario: Consultar las alertas almacenadas

Given que el historial contiene alertas válidas
When el operador solicita consultarlo
Then el sistema muestra primero la alerta más reciente
And presenta el sensor, la fecha y hora, los valores y los umbrales de cada alerta

### Escenario: Consultar un historial sin alertas

Given que el archivo no existe o no contiene alertas
When el operador solicita consultar el historial
Then el sistema informa que no existen alertas almacenadas

### Escenario: Encontrar un registro inválido

Given que el historial contiene registros válidos y uno que no puede interpretarse
When el operador consulta el historial
Then el sistema muestra los registros válidos
And omite e informa el registro inválido

## US-09: Filtrar el historial de alertas

**Como** operador de la bodega industrial,  
**quiero** filtrar las alertas por sensor, periodo o tipo de anomalía,  
**para** localizar información relevante sin revisar todo el historial.

**Prioridad MoSCoW:** Should  
**Story points:** 5

### Escenario: Aplicar uno o varios filtros

Given que el historial contiene alertas de distintos sensores, fechas y tipos
When el operador filtra por sensor, periodo, tipo de anomalía o una combinación
Then el sistema muestra únicamente las alertas que cumplen todos los criterios indicados
And evalúa el periodo mediante la fecha y hora de la lectura
And incluye sus límites inicial y final
And conserva completas las alertas consolidadas

### Escenario: No encontrar coincidencias

Given que el operador proporcionó filtros válidos
When ninguna alerta cumple los criterios
Then el sistema informa que no encontró coincidencias

### Escenario: Rechazar filtros inválidos

Given que la fecha inicial es posterior a la final o el tipo no es "temperatura" ni "humedad"
When el operador solicita filtrar el historial
Then el sistema informa que los criterios son inválidos
And no realiza la consulta

## US-10: Generar un resumen estadístico

**Como** operador de la bodega industrial,  
**quiero** obtener un resumen del historial completo o filtrado,  
**para** identificar las anomalías y los sensores que requieren mayor atención.

**Prioridad MoSCoW:** Should  
**Story points:** 5

### Escenario: Generar el resumen

Given que existen alertas para analizar
When el operador solicita el resumen
Then el sistema muestra el total de alertas
And muestra la cantidad y el valor máximo por tipo de anomalía
And identifica al sensor o los sensores con más alertas
And cuenta una alerta consolidada una vez, pero contabiliza sus dos anomalías

### Escenario: Resumir resultados filtrados

Given que el operador obtuvo alertas mediante la US-09
When solicita el resumen de esos resultados
Then el sistema utiliza únicamente las alertas coincidentes

### Escenario: Solicitar un resumen sin datos

Given que no existen alertas en el historial o en la selección
When el operador solicita el resumen
Then el sistema informa que no hay información para analizar

## US-11: Detectar sensores inactivos

**Como** operador de la bodega industrial,  
**quiero** recibir un aviso cuando un sensor deje de enviar lecturas,  
**para** detectar oportunamente fallos de comunicación o funcionamiento.

**Prioridad MoSCoW:** Should  
**Story points:** 5

### Escenario: Detectar un sensor inactivo

Given que un sensor está bajo supervisión
When el tiempo desde su última lectura o desde el inicio de su supervisión alcanza el límite configurado
Then el sistema lo identifica como inactivo
And muestra un solo aviso durante ese periodo de inactividad

### Escenario: Detectar la recuperación

Given que un sensor está marcado como inactivo
When el sistema recibe una nueva lectura
Then lo marca como activo
And informa que recuperó la comunicación
And permite detectar un nuevo periodo de inactividad posteriormente

### Escenario: Supervisar varios sensores

Given que existen varios sensores bajo supervisión
When solo uno supera el límite de inactividad
Then el sistema mantiene el estado individual de cada sensor
And avisa únicamente sobre el sensor inactivo

## US-12: Exportar un reporte de alertas y estadísticas

**Como** operador de la bodega industrial,  
**quiero** exportar las alertas y su resumen estadístico,  
**para** consultar y compartir la información fuera del sistema.

**Prioridad MoSCoW:** Could  
**Story points:** 5

### Escenario: Exportar un reporte

Given que existen alertas en el historial completo o en una selección filtrada
When el operador solicita la exportación
Then el sistema genera un CSV con las alertas y otro con el resumen
And utiliza la misma selección para ambos archivos
And conserva cada alerta consolidada en una sola fila
And utiliza nombres únicos para no sobrescribir reportes anteriores

### Escenario: Exportar sin alertas

Given que no existen alertas para exportar
When el operador solicita el reporte
Then el sistema informa que no hay información disponible
And no genera archivos vacíos

### Escenario: Fallar la exportación

Given que la ubicación de destino no permite crear los archivos
When el operador solicita el reporte
Then el sistema informa el error
And no indica que la exportación terminó correctamente