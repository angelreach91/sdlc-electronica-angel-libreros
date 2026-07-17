# Bitácora de uso de IA

> Registro de interacciones significativas con herramientas de inteligencia artificial durante el curso.  
> Cada entrada documenta el prompt utilizado, la propuesta generada, la decisión tomada y su justificación técnica.

---

## Semana 1

### Entrada 1 — Propuesta inicial del ejercicio de sensores

#### Objetivo

Obtener una primera propuesta de estructura para el ejercicio del lunes sobre lecturas de sensores.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a crear una primera versión de un ejercicio en Python sobre lecturas de sensores.
>
> Quiero usar:
>
> - un `Enum` para distinguir sensores de temperatura y humedad;
> - una `dataclass` inmutable llamada `Reading`;
> - un `Protocol` llamado `Transport`;
> - cinco funciones puras para convertir temperatura, comparar umbrales, serializar una lectura, clasificarla y escalar su valor.
>
> Usa type hints completos, evita modificar los objetos originales y no uses `print` dentro de las funciones. También quiero que el código pueda revisarse con `mypy` y `ruff`.
>
> Haz solo una propuesta inicial, sin pruebas por ahora.

#### Propuesta de la IA

Copilot generó una estructura con:

- `Enum` para los tipos de sensores;
- `@dataclass(frozen=True, slots=True)` para representar lecturas;
- `Protocol` para definir un transporte;
- cinco funciones relacionadas con conversión, comparación de umbrales, serialización, clasificación y escalamiento;
- type hints y docstrings.

También agregó elementos no solicitados, como:

- `from __future__ import annotations`;
- `slots=True`;
- una serialización que devolvía `str` en lugar de `bytes`;
- funciones que no trabajaban directamente con `Reading`;
- decisiones adicionales de diseño que no estaban definidas en la guía.

#### Decisión tomada

La propuesta no se aceptó de forma completa. Se decidió conservar únicamente las partes que coincidían con los objetivos del ejercicio y modificar o eliminar aquellas que agregaban complejidad innecesaria o se alejaban de las instrucciones.

#### Cambios realizados

- Se eliminó `from __future__ import annotations`.
- Se eliminó `slots=True`.
- Se recuperó el campo `sensor_id`.
- Se cambió el parámetro `payload` de `str` a `bytes`.
- Se ajustó la serialización para devolver `bytes`.
- Se simplificaron las funciones de comparación y clasificación.
- Se decidió que las funciones principales trabajaran directamente con objetos `Reading`.
- Se omitieron construcciones cuya utilidad todavía no podía explicar con claridad.

#### Justificación

La estructura propuesta por Copilot era funcional, pero incluía características que no eran necesarias para cumplir con la guía. Algunas líneas, como `from __future__ import annotations` y `slots=True`, introducían conceptos adicionales que todavía no domino.

También se modificaron varios contratos para alinearlos con la actividad. Por ejemplo, `Transport` debía trabajar con `bytes`, la serialización debía devolver `bytes` y las funciones debían operar directamente sobre `Reading`.


### Entrada 2 — Propuesta de pruebas para el ejercicio de sensores

#### Objetivo

Obtener una primera propuesta de pruebas con `pytest` para comprobar el funcionamiento de las principales funciones del archivo `sensores.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Ayúdame a crear una primera propuesta de pruebas con pytest para mi archivo sensores.py.
>
> Quiero revisar que funcionen bien estas cinco funciones:
>
> - `celsius_to_fahrenheit`
> - `exceeds_threshold`
> - `to_frame`
> - `classify_reading`
> - `scale_reading`
>
> Incluye casos normales, algunos casos límite y un caso de error cuando tenga sentido.
>
> También quiero comprobar que `scale_reading` no cambie la lectura original y que `celsius_to_fahrenheit` marque error si recibe una lectura que no sea de temperatura.
>
> Crea las pruebas en un archivo llamado `test_sensores.py`. No cambies `sensores.py` y no agregues comportamientos que mi código todavía no tenga.

#### Propuesta de la IA

Copilot propuso siete pruebas:

1. Conversión correcta de Celsius a Fahrenheit.
2. Error al intentar convertir una lectura de humedad.
3. Comparación de una lectura por encima del umbral.
4. Comparación de una lectura igual o inferior al umbral.
5. Serialización de una lectura en formato `bytes`.
6. Clasificación de lecturas como `LOW`, `NORMAL` y `HIGH`.
7. Escalamiento de una lectura sin modificar el objeto original.

También agregó imports y una modificación manual de `sys.path` para localizar el archivo `sensores.py`.

#### Decisión tomada

Se decidió conservar únicamente cuatro pruebas:

- conversión correcta de Celsius a Fahrenheit;
- error al recibir una lectura de humedad;
- detección de un valor superior al umbral;
- clasificación de una lectura como alta.

Las demás pruebas no se descartaron por ser incorrectas, sino porque incluían estructuras y comprobaciones que todavía no puedo explicar con claridad.

#### Cambios realizados

- Se eliminaron las pruebas de serialización y escalamiento.
- Se redujo la prueba de clasificación a un solo caso sencillo.
- Se eliminó la modificación manual de `sys.path`.
- Se conservaron únicamente los imports necesarios.
- Se mantuvo una estructura sencilla basada en creación de datos, ejecución de la función y verificación mediante `assert`.

#### Justificación

La propuesta de Copilot era más completa de lo necesario para esta etapa. Algunas pruebas, especialmente la de escalamiento e inmutabilidad, incluían comprobaciones como `is not` y comparación de múltiples atributos. Aunque esas pruebas podían ser correctas, todavía no puedo explicar con seguridad cada una de esas decisiones.

Se decidió conservar cuatro pruebas sencillas y distintas entre sí. Estas permiten comprobar un cálculo correcto, una condición de error, una comparación booleana y una clasificación.


### Entrada 3 — Propuesta para completar la máquina de estados finita

#### Objetivo

Obtener una propuesta para completar la clase `TrafficLightFSM`, encargada de representar el funcionamiento de un semáforo mediante programación orientada a objetos.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Estoy desarrollando una máquina de estados finita para representar el funcionamiento de un semáforo mediante programación orientada a objetos en Python.
>
> Hasta ahora definí una enumeración llamada `TrafficLightState` con los estados `RED`, `YELLOW` y `GREEN`. También creé una clase llamada `TrafficLightFSM` con un constructor que inicia el estado del semáforo en `RED` y un contador de transiciones en `0`.
>
> Me quedé bloqueado y no sé cómo continuar la estructura de la clase. Sugiere el código necesario para consultar el estado actual sin modificarlo directamente, consultar el contador de transiciones y realizar la secuencia `RED → GREEN → YELLOW → RED`, aumentando el contador en cada transición.
>
> Por el momento no escribas pruebas. Mantén la solución sencilla, con anotaciones de tipo y fácil de comprender y explicar.

#### Propuesta de la IA

Copilot propuso completar la clase con:

- una propiedad `state` para consultar el estado actual;
- una propiedad `transitions` para consultar el número de transiciones realizadas;
- un método llamado `advance`;
- condicionales `if` y `elif` para determinar el siguiente estado;
- incremento del contador después de cada transición;
- anotaciones de tipo y docstrings.

La secuencia propuesta fue:

- `RED` a `GREEN`;
- `GREEN` a `YELLOW`;
- `YELLOW` a `RED`.

#### Decisión tomada

La propuesta no se aceptó de forma completa. Se decidió conservar las propiedades, las anotaciones de tipo, los docstrings y el incremento del contador.

#### Cambios realizados

- Se conservó la propiedad `state`.
- Se cambió la propiedad `transitions` por `cycle_count`.
- Se cambió el método `advance` por `transition`.
- Se modificó el tipo de retorno del método de `None` a `TrafficLightState`.
- Se reemplazó la estructura basada en `if` y `elif` por un diccionario de transiciones.
- Se agregó el retorno del nuevo estado después de cada transición.
- Se conservaron docstrings sencillas para explicar el propósito de cada propiedad y método.
- No se copiaron los marcadores `# ...existing code...`.

#### Justificación

La propuesta de Copilot era funcional, pero algunos elementos no coincidían completamente con la estructura planteada en la actividad.

El método se cambió de `advance` a `transition` para utilizar un nombre más relacionado con una máquina de estados. La propiedad `cycle_count` se eligió para mantener consistencia con el atributo interno `_cycle_count`.

También se decidió utilizar un diccionario de transiciones porque permite representar directamente la relación entre el estado actual y el siguiente estado. De esta forma, la secuencia queda definida sin utilizar varios bloques condicionales.

Finalmente, se agregó el retorno del nuevo estado para que el resultado de cada transición pueda consultarse directamente y utilizarse posteriormente en las pruebas

### Entrada 4 — Propuesta y corrección de pruebas para la máquina de estados

#### Objetivo

Obtener una primera propuesta de pruebas con `pytest` para comprobar el funcionamiento de la máquina de estados finita implementada en `fsm_demo.py`.

#### Herramienta utilizada

`GitHub Copilot`

#### Prompt utilizado

> Estoy trabajando en una máquina de estados finita para un semáforo en Python. Ya tengo una clase llamada `TrafficLightFSM` que inicia en `RED`, cambia siguiendo la secuencia `RED → GREEN → YELLOW → RED` y lleva un contador de transiciones.
>
> Ahora necesito crear el archivo `test_fsm.py` con pruebas usando `pytest`, pero todavía no sé bien cómo estructurarlas.
>
> Ayúdame a proponer cuatro pruebas sencillas para comprobar:
>
> - que el estado inicial sea `RED`;
> - que una transición cambie de `RED` a `GREEN`;
> - que tres transiciones completen el ciclo y regresen a `RED`;
> - que el contador de transiciones aumente correctamente.
>
> No modifiques `fsm_demo.py`. Mantén las pruebas simples, fáciles de entender y con nombres descriptivos. No agregues casos adicionales por ahora.

#### Propuesta de la IA

Copilot propuso cuatro pruebas:

1. Comprobar que el estado inicial fuera rojo.
2. Comprobar la transición de rojo a verde.
3. Comprobar que tres transiciones completaran el ciclo y regresaran a rojo.
4. Comprobar que el contador aumentara después de ejecutar transiciones.

La estructura general de las pruebas era adecuada, pero la primera propuesta contenía algunos errores relacionados con los nombres y elementos definidos en mi implementación.

Copilot no importó inicialmente `TrafficLightState` y en las comprobaciones utilizó directamente nombres como `RED` y `GREEN`. También utilizó una propiedad llamada `counter`, aunque en mi clase la propiedad definida se llamaba `cycle_count`.

#### Decisión tomada

La propuesta no se aceptó directamente. Se revisó cada prueba y se corrigieron los nombres para que coincidieran con la implementación real de `fsm_demo.py`.

Se conservaron las cuatro pruebas porque correspondían con los puntos solicitados en la guía, pero se modificaron las importaciones y las expresiones utilizadas en los `assert`.

#### Cambios realizados

- Se agregó `TrafficLightState` a la importación desde `fsm_demo.py`.
- Se reemplazó el uso de `counter` por `cycle_count`.
- Se corrigieron las comprobaciones de estado para utilizar los miembros completos de la enumeración.
- En la primera prueba se cambió la comparación a `TrafficLightState.RED`.
- En la segunda prueba se cambió la comparación a `TrafficLightState.GREEN`.
- En la tercera prueba se cambió la comparación final a `TrafficLightState.RED`.
- Se conservaron los nombres descriptivos de las cuatro funciones de prueba.
- Se mantuvo una instancia nueva de `TrafficLightFSM` dentro de cada prueba para que fueran independientes.

#### Justificación

Durante el primer intento de ejecución y revisión de las pruebas se detectó que Copilot no había tomado en cuenta completamente los nombres utilizados en mi código.

La clase no tenía una propiedad llamada `counter`, por lo que Pylance marcaba error al intentar acceder a ese atributo. La propiedad correcta era `cycle_count`, ya que ese era el nombre definido previamente en `TrafficLightFSM`.

También fue necesario importar `TrafficLightState`, porque los estados `RED`, `GREEN` y `YELLOW` no estaban definidos como variables independientes. Estos valores pertenecen a la enumeración, por lo que deben escribirse como `TrafficLightState.RED`, `TrafficLightState.GREEN` respectivamente dependiendo lo que quieras comprobar con assert.

###### Objetivo

Utilizar herramientas de inteligencia artificial como apoyo para proponer y adaptar una solución que demostrara los principios de responsabilidad única, abierto/cerrado y sustitución de Liskov en el dominio de sensores.

La actividad debía incluir un ejemplo “mal”, un ejemplo “bien” y dos pruebas por cada principio en los archivos:

- `semana1/miercoles_15_de_julio/solid_srp_ocp_lsp.py`
- `semana1/miercoles_15_de_julio/test_solid_srp_ocp_lsp.py`

#### Herramientas utilizadas

- GitHub Copilot, para obtener una primera propuesta de estructura y código.
- Codex, para revisar la propuesta inicial y aplicar las adaptaciones seleccionadas.

#### Prompt utilizado con GitHub Copilot

> Ayúdame a proponer la estructura y el código completo para la actividad del miércoles sobre los principios SOLID S, O y L aplicados a sensores.
>
> Voy a trabajar con los archivos `solid_srp_ocp_lsp.py` y `test_solid_srp_ocp_lsp.py`. En el primer archivo necesito un ejemplo “mal” y uno “bien” de cada principio. Para S se deben separar las responsabilidades de `SensorReader` y `DataLogger`; para O se debe utilizar `AlertStrategy`, `ConsoleAlert`, `FileAlert` y `AnomalyDetector`; y para L se debe comprobar que `TemperatureSensor` y `HumiditySensor` funcionen donde se espere `BaseSensor`.
>
> En el segundo archivo necesito dos pruebas con pytest por cada principio, seis en total. Utiliza type hints, clases abstractas cuando sea necesario y valores simulados para no depender de sensores reales. Primero muéstrame la estructura y después el código completo de ambos archivos.

#### Propuesta de GitHub Copilot

Copilot propuso una primera solución con:

- Una clase que mezclaba la lectura y el almacenamiento de datos como ejemplo incorrecto de responsabilidad única.
- `SensorReader` y `DataLogger` como separación correcta de responsabilidades.
- Un detector con una alerta integrada como ejemplo incorrecto del principio abierto/cerrado.
- Una estrategia de alertas con implementaciones para consola y archivo.
- Una clase base para sensores y dos implementaciones intercambiables.
- Seis pruebas, distribuidas en dos pruebas por principio.

La propuesta servía como punto de partida, pero era extensa y contenía elementos que no aportaban directamente a la actividad o que no coincidían completamente con la estructura indicada en la guía.

#### Revisión y comprensión de la propuesta

La propuesta no se incorporó de forma inmediata. Primero se revisó la responsabilidad de cada clase, la relación entre las abstracciones y sus implementaciones, y el propósito de cada prueba.

Durante este análisis se identificó que:

- No se utilizaba `SensorReading` para representar las mediciones.
- Los métodos de las alertas y del detector tenían nombres distintos a los mostrados en la guía.
- `AlertStrategy` no se había implementado mediante `ABC` y `abstractmethod`.
- `FileAlert` simulaba un archivo mediante una lista en lugar de escribir realmente en uno.
- El ejemplo incorrecto de Liskov no heredaba de `BaseSensor`.
- `process_sensor()` devolvía una estructura más compleja de lo necesario.
- El archivo de pruebas utilizaba una carga dinámica del módulo que dificultaba su comprensión.
- Existían importaciones, tipos y configuraciones que no contribuían directamente a demostrar SOLID.

La revisión también permitió comprender que los ejemplos “mal” no debían ser código escrito incorrectamente. Debían funcionar, pero mostrar una decisión de diseño que violara el principio correspondiente.

#### Prompt utilizado con Codex

> Adapta los archivos `solid_srp_ocp_lsp.py` y `test_solid_srp_ocp_lsp.py` a partir de los problemas identificados en la propuesta de Copilot.
>
> Agrega `SensorReading`, identifica claramente los ejemplos “mal” y “bien”, utiliza `ABC` para las abstracciones, haz que `FileAlert` escriba realmente en un archivo y utiliza importaciones normales en las pruebas. Mantén dos pruebas por principio y elimina los elementos que no aporten al objetivo. No crees archivos adicionales ni realices el commit.

#### Propuesta de Codex

Codex reorganizó la solución para:

- Representar las mediciones mediante una dataclass inmutable.
- Separar la lectura y el almacenamiento en el ejemplo correcto de SRP.
- Mostrar explícitamente los condicionales que violan OCP.
- Implementar `AlertStrategy` como una clase abstracta.
- Permitir que `AnomalyDetector` trabajara con alertas de consola o archivo.
- Hacer que los sensores de temperatura y humedad respetaran el contrato de `BaseSensor`.
- Simplificar `process_sensor()` para que devolviera directamente una lectura.
- Sustituir la carga dinámica del módulo por importaciones normales.
- Mantener exactamente seis pruebas.

#### Decisión tomada

Se decidió conservar la estructura general propuesta por las herramientas de IA, pero no aceptar automáticamente todo el código generado.

Se mantuvieron los elementos que ayudaban a demostrar claramente los principios SOLID y se eliminaron o modificaron los que añadían complejidad innecesaria. También se conservaron comentarios y divisiones visibles para facilitar la identificación de los ejemplos “mal” y “bien”.

Antes de aceptar la solución, se revisó qué responsabilidad tenía cada clase, por qué el ejemplo incorrecto violaba el principio y cómo el ejemplo correcto solucionaba el problema.

#### Cambios realizados

- Se agregó `SensorReading` para representar el identificador y el valor de cada medición.
- Se separaron `SensorReader` y `DataLogger`.
- Se creó un detector incorrecto basado en condicionales.
- Se implementaron `AlertStrategy`, `ConsoleAlert`, `FileAlert` y `AnomalyDetector`.
- Se hizo que `FileAlert` escribiera en un archivo temporal durante las pruebas.
- Se definió el contrato común `BaseSensor`.
- Se incluyó un sensor incorrecto que no respeta ese contrato.
- Se implementaron `TemperatureSensor` y `HumiditySensor` como sustituciones válidas.
- Se escribieron dos pruebas por cada principio.
- Se identificaron explícitamente mediante comentarios los ejemplos “mal” y “bien”.

#### Justificación

La inteligencia artificial se utilizó para generar una primera propuesta y acelerar la reorganización del código, pero la solución no se aceptó sin revisión.

El proceso incluyó la lectura y comprensión de las propuestas, la identificación de decisiones que no coincidían con la consigna y la selección de los elementos que realmente ayudaban a demostrar cada principio. La versión final fue el resultado de combinar las propuestas de las herramientas con una revisión razonada de su funcionamiento y de su utilidad para la actividad.

### Entrada 5 — Revisión de ISP y DIP

#### Objetivo

Revisar la estructura del archivo `solid_isp_dip.py` y comprobar que su funcionamiento cumpliera correctamente con los principios ISP y DIP.

#### Herramienta utilizada

Codex con el modelo GPT-5.6 Sol.

#### Prompts utilizados

Primera solicitud:

> Revisa el archivo completo y verifica si la estructura cumple correctamente con ISP y DIP. Indica si existe algún error, código innecesario o elemento indispensable que falte. No modifiques el archivo y recomienda solamente cambios sencillos que pueda comprender y explicar.

Segunda solicitud:

> Comprueba el funcionamiento del repositorio y de `DataProcessor` mediante pruebas mínimas. Verifica el almacenamiento, la consulta de sensores inexistentes, el reemplazo de lecturas y la inyección de dependencias. No modifiques el código ni crees archivos adicionales.

#### Propuesta de la IA

En la primera revisión, Codex determinó que la estructura cumplía correctamente con ISP y DIP. Como ajuste principal, recomendó cambiar el nombre del protocolo `ReadableSensor` por `Readable` para coincidir exactamente con el enunciado. También señaló algunos espacios y líneas vacías que podían corregirse.

En la segunda solicitud, Codex comprobó que `InMemoryRepository` guardaba y recuperaba lecturas, devolvía `None` para sensores inexistentes y reemplazaba la lectura anterior cuando se utilizaba el mismo identificador. También confirmó que `DataProcessor` funcionaba correctamente al recibir el repositorio mediante inyección de dependencias. Todas las comprobaciones resultaron satisfactorias.

#### Decisión tomada

Se aceptó el cambio de `ReadableSensor` por `Readable` porque coincidía con el nombre solicitado en la actividad. También se corrigieron los detalles de formato señalados. Las recomendaciones y los resultados fueron revisados y comprendidos antes de considerarse válidos.

#### Cambios realizados

- Se renombró `ReadableSensor` como `Readable`.
- Se eliminaron espacios sobrantes.
- Se ajustaron las líneas vacías entre las clases.
- No se agregaron clases, dependencias ni implementaciones adicionales.

#### Justificación

Codex se utilizó como una herramienta de revisión y comprobación, no para reemplazar la comprensión del ejercicio. Sus observaciones permitieron confirmar que las interfaces estaban correctamente segregadas y que `DataProcessor` dependía de la abstracción `DataRepository`. La solución se mantuvo sencilla y limitada a los requisitos de la actividad.
