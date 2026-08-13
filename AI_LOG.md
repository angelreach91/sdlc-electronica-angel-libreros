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

### 17 de julio de 2026 — Análisis y planificación del driver UART

#### Objetivo

Comprender los requisitos de la actividad del viernes antes de comenzar a programar y definir una estructura que permitiera desarrollar un driver UART modular, verificable y con un nivel de alcance alto.

#### Herramienta utilizada

ChatGPT y Codex.

#### Prompt utilizado

> Analiza las instrucciones de la actividad del viernes y el checklist de cierre de la semana. Quiero desarrollar y entender paso a paso el driver UART solicitado. Primero necesito comprender el problema, identificar qué componentes debemos entregar y construir una base sólida que posteriormente pueda ser revisada y complementada con Codex.

#### Propuesta de la IA

La IA propuso dividir el problema en componentes independientes para evitar concentrar todas las responsabilidades en un solo archivo. La estructura sugerida contempló módulos para:

- La configuración y validación de los parámetros UART.
- La interpretación de diferentes protocolos.
- La representación del dispositivo UART.
- El almacenamiento de los mensajes procesados.
- El manejo de un búfer circular.
- La generación de registros estructurados.
- Las pruebas automatizadas de cada componente.

También se propuso trabajar de manera incremental: implementar un componente, comprender su responsabilidad, probarlo y después continuar con el siguiente.

#### Decisión tomada

Se aceptó la división modular porque correspondía con los principios SOLID estudiados durante la semana. Sin embargo, se decidió no generar todo el driver de una sola vez.

El desarrollo se realizó por etapas para poder revisar cada propuesta, comprender el propósito de las clases y detectar posibles errores antes de avanzar. Codex se reservó principalmente para revisar y complementar partes específicas del trabajo.

#### Cambios realizados

- Se creó la estructura general del paquete `uart_driver`.
- Se identificaron las responsabilidades principales del sistema.
- Se estableció un orden de desarrollo para evitar mezclar configuración, procesamiento, almacenamiento y registro.
- Se definió que los parsers serían dependencias intercambiables del dispositivo.

#### Justificación

La IA se utilizó inicialmente como apoyo para interpretar una actividad que todavía no se comprendía por completo. La división propuesta permitió convertir un problema amplio en componentes pequeños y manejables.

La decisión final fue construir el proyecto paso a paso para que el código no se limitara a una respuesta generada automáticamente, sino que pudiera ser revisado y comprendido durante su implementación.

---

### 17 de julio de 2026 — Configuración y validación de parámetros UART

#### Objetivo

Crear una representación clara de la configuración UART y evitar que pudiera construirse un dispositivo con valores inválidos.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a crear el módulo de configuración del driver UART. Debe representar la paridad, los bits de parada y los demás parámetros necesarios. Quiero que la configuración sea inmutable y que valide sus datos desde el momento en que se crea.

#### Propuesta de la IA

La IA propuso utilizar enumeraciones para representar la paridad y los bits de parada. También sugirió utilizar una `dataclass` inmutable para agrupar los parámetros de configuración.

La primera propuesta concentraba las validaciones dentro de un solo método. Posteriormente se sugirió separar las comprobaciones en métodos pequeños para que cada uno validara una condición concreta.

#### Decisión tomada

Se conservaron las enumeraciones porque limitan los valores posibles y evitan utilizar cadenas arbitrarias. También se aceptó el uso de una `dataclass` con `frozen=True` para impedir que una configuración válida cambie después de crear el dispositivo.

Después de revisar la primera versión, se decidió dividir la validación en cuatro métodos auxiliares. Este cambio hizo que el código fuera más fácil de leer y permitió identificar con claridad qué condición produce cada excepción.

#### Cambios realizados

- Se creó `config.py`.
- Se definió la enumeración `Parity`.
- Se definió la enumeración `StopBits`.
- Se creó la clase inmutable `UartConfig`.
- Se incorporaron validaciones para impedir configuraciones UART inválidas.
- Se dividió la lógica de validación en métodos con responsabilidades específicas.
- Se agregaron pruebas para configuraciones válidas e inválidas.

#### Justificación

La IA ayudó a elegir estructuras adecuadas para representar valores limitados y datos de configuración. La propuesta fue revisada y refactorizada antes de considerarse terminada.

El resultado evita que los errores de configuración lleguen a etapas posteriores del procesamiento. Esto simplifica el resto del driver porque los demás componentes pueden asumir que recibieron una configuración válida.

---

### 17 de julio de 2026 — Implementación de parsers para diferentes protocolos

#### Objetivo

Permitir que el driver procesara distintos tipos de mensajes sin incorporar la lógica de cada protocolo directamente dentro del dispositivo UART.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Necesito desarrollar los parsers del driver UART para Modbus RTU, NMEA GPGGA y una trama CAN simplificada. Explícame qué debe validar cada protocolo y ayúdame a implementar cada parser por separado para que pueda entender su funcionamiento.

#### Propuesta de la IA

La IA propuso que cada parser encapsulara las reglas de su propio protocolo:

- Para Modbus RTU, comprobar la longitud de la trama y validar el CRC-16.
- Para NMEA GPGGA, verificar el checksum XOR, separar los campos y convertir la latitud y longitud a grados decimales.
- Para CAN simplificado, comprobar la cabecera, interpretar un identificador de 11 bits, leer el DLC y validar la longitud de los datos.

La IA también explicó que el dispositivo no debía conocer los detalles de cada formato. Su responsabilidad sería recibir bytes y delegar su interpretación al parser configurado.

#### Decisión tomada

Se aceptó mantener los parsers separados porque los tres protocolos utilizan estructuras y mecanismos de validación diferentes.

Se decidió implementar solamente las características solicitadas por la actividad. No se intentó construir una implementación completa de los estándares Modbus, NMEA o CAN, ya que eso habría aumentado innecesariamente el alcance.

Cada algoritmo fue revisado de forma individual. En Modbus se estudió el desplazamiento de bits y el polinomio `0xA001`; en NMEA se revisó el cálculo XOR y la conversión de coordenadas; en CAN se comprobó que el identificador permaneciera dentro del rango correspondiente a 11 bits.

#### Cambios realizados

- Se creó `parsers.py`.
- Se implementó el cálculo y la comprobación CRC-16 para Modbus RTU.
- Se implementó la validación del checksum de sentencias NMEA GPGGA.
- Se incorporó la conversión de coordenadas NMEA a grados decimales.
- Se implementó el parser de una trama CAN simplificada.
- Se agregaron validaciones para cabeceras, longitudes y contenido inválido.
- Se crearon pruebas con tramas válidas y tramas alteradas.

#### Justificación

La IA permitió explicar algoritmos que no eran evidentes únicamente al observar el código, especialmente el CRC de Modbus y la representación de coordenadas NMEA.

Las propuestas no se copiaron sin revisión. Se comprobó qué representaba cada byte y por qué una trama debía aceptarse o rechazarse. La separación de parsers permite ampliar el sistema con otros protocolos sin modificar la lógica principal del dispositivo.

---

### 17 de julio de 2026 — Dispositivo UART y almacenamiento de mensajes

#### Objetivo

Crear el componente encargado de representar el dispositivo UART, controlar su estado y procesar mensajes mediante el parser seleccionado.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a implementar el dispositivo UART utilizando la configuración y los parsers que ya desarrollamos. Debe poder conectarse, desconectarse y procesar datos. También necesito almacenar el resultado procesado sin mezclar esa responsabilidad con la interpretación del mensaje.

#### Propuesta de la IA

La IA propuso crear `UartDevice` con tres dependencias principales:

- Una configuración UART.
- Un parser encargado de interpretar los datos.
- Un búfer opcional para almacenar los mensajes procesados.

También sugirió separar el almacenamiento permanente en otro módulo mediante un grabador de registros JSON Lines.

El método de procesamiento debía verificar primero el estado del dispositivo, delegar los bytes al parser y enviar el resultado al búfer cuando este estuviera configurado.

#### Decisión tomada

Se aceptó la inyección del parser porque permite que el mismo dispositivo funcione con diferentes protocolos. También se conservó el búfer como una dependencia opcional para poder utilizar el dispositivo sin obligarlo a almacenar todos los resultados.

Se decidió que `UartDevice` no administrara archivos directamente. El almacenamiento persistente quedó en `recorder.py`, evitando mezclar la comunicación con las operaciones de escritura.

#### Cambios realizados

- Se creó `device.py`.
- Se implementó la clase `UartDevice`.
- Se agregaron las operaciones de conexión y desconexión.
- Se incorporó la validación del estado antes de procesar un mensaje.
- Se delegó la interpretación de los bytes al parser configurado.
- Se permitió almacenar el resultado en un búfer opcional.
- Se creó `recorder.py`.
- Se implementó el almacenamiento mediante el formato JSON Lines.
- Se comprobó que los objetos fueran serializables antes de escribirlos.
- Se agregaron pruebas para el ciclo de conexión, procesamiento y almacenamiento.

#### Justificación

La propuesta permitió aplicar inversión de dependencias: el dispositivo utiliza abstracciones proporcionadas desde el exterior y no crea internamente un parser concreto.

La revisión manual se concentró en verificar el flujo completo: el dispositivo recibe datos, comprueba su estado, solicita al parser que los interprete y entrega el resultado al componente correspondiente. Esta separación reduce el acoplamiento y facilita las pruebas.

---

### 17 de julio de 2026 — Búfer circular seguro para concurrencia

#### Objetivo

Agregar un mecanismo de almacenamiento temporal con capacidad limitada que pudiera utilizarse de manera segura cuando existieran accesos concurrentes.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Necesito implementar un búfer circular genérico para los mensajes procesados por el driver. Debe tener una capacidad máxima y ser seguro si distintas partes del programa intentan acceder al mismo tiempo. Explícame por qué se utilizan `deque`, los genéricos y un bloqueo.

#### Propuesta de la IA

La IA propuso implementar `ThreadSafeCircularBuffer` utilizando:

- `Generic` y `TypeVar` para aceptar diferentes tipos de datos.
- `deque` con una capacidad máxima para descartar automáticamente el elemento más antiguo cuando el búfer se llena.
- `Lock` para proteger las operaciones que consultan o modifican la colección.

También se propusieron operaciones para agregar elementos, consultar el contenido, obtener la cantidad almacenada y limpiar el búfer.

#### Decisión tomada

Se aceptó utilizar `deque` porque ya proporciona el comportamiento circular necesario y evita implementar manualmente índices de lectura y escritura.

El uso de `Lock` se mantuvo porque varias operaciones sobre una colección compartida pueden interferir entre sí. Se revisó que el bloqueo protegiera únicamente las secciones necesarias para no conservarlo durante operaciones externas.

#### Cambios realizados

- Se creó `buffer.py`.
- Se implementó `ThreadSafeCircularBuffer` como una clase genérica.
- Se estableció una capacidad máxima.
- Se incorporó un bloqueo para proteger el estado interno.
- Se implementó el reemplazo del elemento más antiguo cuando se supera la capacidad.
- Se agregaron pruebas para inserción, consulta, límite de capacidad y limpieza.

#### Justificación

La IA ayudó a explicar que “seguro para hilos” no significa únicamente utilizar un contenedor adecuado, sino proteger las operaciones compuestas que leen o modifican el estado compartido.

La solución se mantuvo sencilla y utiliza componentes de la biblioteca estándar de Python. Esto permitió cumplir el requisito de concurrencia sin introducir dependencias adicionales.

---

### 17 de julio de 2026 — Registro estructurado en formato JSON

#### Objetivo

Generar registros legibles por programas y personas, incluyendo información suficiente para identificar cuándo ocurrió un evento y qué parte del sistema lo produjo.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a implementar un formatter de logging que produzca una línea JSON por evento. Necesito que incluya fecha y hora, nivel, nombre del logger y mensaje. También debe conservar correctamente caracteres Unicode.

#### Propuesta de la IA

La IA propuso crear `JsonFormatter` como una especialización de `logging.Formatter`. Cada registro debía convertirse en un diccionario y después serializarse como JSON.

Los campos propuestos fueron:

- `timestamp`, utilizando formato ISO 8601 y la indicación de UTC.
- `level`, para representar el nivel del evento.
- `logger`, para identificar el origen.
- `event`, para almacenar el mensaje.

También se sugirió configurar la serialización para conservar caracteres Unicode legibles.

#### Decisión tomada

Se aceptó el formato JSON porque facilita el procesamiento posterior de los registros y mantiene una estructura constante.

Se decidió usar el nombre `event` para el mensaje principal y conservar los caracteres Unicode sin convertirlos en secuencias escapadas innecesarias. Después de generar el formatter, se revisó que cada línea pudiera interpretarse nuevamente como un objeto JSON válido.

#### Cambios realizados

- Se creó `json_logging.py`.
- Se implementó `JsonFormatter`.
- Se incorporó una marca de tiempo en formato ISO 8601.
- Se agregaron los campos de nivel, logger y evento.
- Se mantuvo la representación legible de caracteres Unicode.
- Se agregaron pruebas para comprobar la estructura y el contenido de los registros.

#### Justificación

La IA se utilizó para proponer una estructura consistente y compatible con el módulo `logging` de Python. La revisión manual permitió comprobar que el resultado no fuera solamente una cadena con apariencia de JSON, sino un objeto que pudiera deserializarse correctamente.

Este componente se mantuvo separado de `recorder.py` porque ambos trabajan con JSON, pero tienen responsabilidades diferentes: uno almacena datos y el otro define el formato de los eventos del sistema.

---

### 17 de julio de 2026 — Revisión del código y pruebas finales con Codex

##### Objetivo

Utilizar Codex para revisar la etapa final del driver y completar exclusivamente las pruebas relacionadas con el dispositivo y el registro estructurado, sin modificar el código de producción que ya se encontraba funcionando.

##### Herramienta utilizada

Codex.

##### Prompt utilizado

> Revisa la implementación actual del driver UART y completa exclusivamente el archivo `test_device_logging.py`. Agrega las pruebas necesarias para comprobar el comportamiento de `UartDevice` y `JsonFormatter`. No modifiques los archivos de producción ni realices cambios fuera del alcance solicitado.

##### Propuesta de la IA

Codex propuso completar `test_device_logging.py` con casos orientados a comprobar:

- El estado de conexión y desconexión del dispositivo.
- El procesamiento de datos mediante el parser configurado.
- El envío del resultado al búfer cuando existe uno.
- La generación de registros JSON con los campos esperados.

Durante la revisión también se identificaron anotaciones que Pylance consideraba incompatibles dentro del archivo de pruebas.

##### Decisión tomada

La propuesta se revisó antes de integrarla. Se confirmó que Codex hubiera trabajado solamente sobre el archivo solicitado y que no reemplazara la implementación construida durante las etapas anteriores.

Inicialmente se consideró ocultar algunas advertencias mediante comentarios de supresión de tipos. Esa opción se descartó porque solamente ocultaba el problema. Se prefirió corregir las anotaciones y los objetos auxiliares utilizados por las pruebas.

##### Cambios realizados

- Se completó `test_device_logging.py`.
- Se verificó el ciclo de conexión y desconexión.
- Se comprobó el procesamiento mediante una dependencia controlada.
- Se validó la integración entre el dispositivo y el búfer.
- Se comprobó que los eventos generados fueran JSON válido.
- Se corrigieron las anotaciones del archivo de pruebas sin utilizar comentarios para ignorar errores.
- Se ejecutó nuevamente la suite completa y todas las pruebas finalizaron correctamente.
- Se confirmó que Pylance no mostrara advertencias en los archivos revisados.

##### Justificación

Codex se utilizó como una segunda revisión del trabajo y no como sustituto del proceso de desarrollo. Limitar su alcance a un archivo permitió comparar su propuesta con el comportamiento que ya se había definido.

La revisión final ayudó a identificar casos que debían comprobarse y problemas de tipado presentes únicamente en las pruebas. Cada cambio fue revisado antes de conservarlo y posteriormente se ejecutaron nuevamente todas las pruebas para confirmar que el driver siguiera funcionando como un conjunto.

---

##### Reflexión sobre el uso de inteligencia artificial

La inteligencia artificial se utilizó durante el desarrollo del driver UART para comprender los requisitos, dividir el problema, proponer estructuras, explicar algoritmos y complementar las pruebas.

El proceso no consistió en solicitar el proyecto completo y copiar el resultado. Primero se analizó la actividad y después se desarrolló cada módulo por separado. Las propuestas de la IA fueron revisadas, ejecutadas y, cuando fue necesario, modificadas.

Los principales usos de la IA fueron:

- Convertir los requisitos de la actividad en componentes concretos.
- Explicar conceptos como CRC-16, checksum XOR, coordenadas NMEA, genéricos y bloqueos.
- Proponer estructuras compatibles con los principios SOLID.
- Identificar validaciones y casos de prueba.
- Revisar la integración final sin modificar componentes fuera del alcance solicitado.

La decisión sobre qué propuestas conservar permaneció bajo revisión humana. Algunas soluciones se refactorizaron para mejorar su claridad y otras se descartaron cuando únicamente ocultaban una advertencia sin resolver su causa.

Como resultado, el driver quedó dividido en componentes con responsabilidades específicas y acompañado de pruebas automatizadas. El uso de la IA también permitió identificar qué partes todavía necesitan mayor estudio, especialmente el funcionamiento interno de UART y los protocolos procesados.

## Semana 2

### Entrada: Elaboración y revisión del backlog del sistema de monitoreo ambiental

#### Objetivo

Construir un backlog para un sistema de monitoreo ambiental en una bodega industrial, utilizando historias de usuario, prioridades MoSCoW, estimaciones mediante story points y escenarios escritos con la estructura Given-When-Then.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a construir y revisar las historias de usuario del sistema de monitoreo ambiental. Para cada historia analiza si el objetivo es claro, si puede verificarse, si existe alguna ambigüedad y qué caso borde relevante podría faltar. Antes de aprobar cada historia, quiero revisar críticamente su alcance, prioridad, estimación y escenarios.

#### Propuesta de la IA

La IA propuso construir el backlog de manera progresiva, revisando cada historia antes de continuar con la siguiente. Para cada una presentó:

- El rol del usuario.
- La necesidad que debía atender.
- El valor aportado al sistema.
- La prioridad MoSCoW.
- Una estimación mediante story points.
- Escenarios principales, alternativos y de error.

Durante el proceso también señaló ambigüedades y casos borde. Entre ellos se encontraron los valores iguales al umbral, lecturas inválidas, sensores inexistentes, alertas consolidadas, archivos dañados, filtros incorrectos, ausencia de resultados y recuperación de sensores inactivos.

A partir de esta revisión se definieron doce historias relacionadas con el registro de sensores y lecturas, validación de datos, configuración de umbrales, detección de anomalías, generación y almacenamiento de alertas, consulta y filtrado del historial, generación de estadísticas, supervisión de sensores inactivos y exportación de reportes.

#### Decisión tomada

No se aceptaron automáticamente las historias propuestas. Cada una fue revisada antes de aprobarla y, cuando existieron dudas, se solicitaron aclaraciones o modificaciones.

Se decidió conservar doce historias porque representan capacidades diferentes del sistema. También se establecieron reglas generales para evitar repetir en cada historia comportamientos como la conservación de alertas consolidadas, el uso de los umbrales vigentes y la obligación de no modificar el historial durante una consulta.

#### Cambios realizados

- Se elaboraron doce historias de usuario.
- Se asignó una prioridad MoSCoW a cada historia.
- Se estimaron las historias con un total de 50 story points.
- Se utilizaron escenarios Given-When-Then para hacer verificables los comportamientos.
- Se definieron reglas generales aplicables a todo el backlog.
- Se aclaró que una variable solamente es anómala cuando supera su umbral.
- Se estableció que una lectura puede producir como máximo una alerta consolidada.
- Se diferenció una anomalía ambiental de un aviso por inactividad.
- Se relacionaron las historias de consulta, filtrado, estadísticas y exportación.

#### Justificación

El uso de la IA permitió contrastar las historias desde diferentes perspectivas y encontrar condiciones que inicialmente no se habían considerado. Sin embargo, las decisiones finales se tomaron después de analizar si cada comportamiento era necesario, comprensible y coherente con el alcance del sistema.

La intención no fue aceptar una especificación generada automáticamente, sino utilizar la IA como apoyo para cuestionar el backlog y mejorar su verificabilidad antes de considerarlo terminado.

---

### Entrada: Simplificación y depuración del backlog

#### Objetivo

Reducir el tamaño del backlog original, eliminar contenido redundante y conservar solamente los escenarios necesarios para explicar y comprobar el comportamiento esperado del sistema.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Revisa detalladamente todas las historias porque el backlog tiene aproximadamente 800 líneas y demasiados escenarios específicos. Analiza nuevamente si cada escenario es verificable, ambiguo o si realmente representa un caso borde importante. Identifica redundancias y reduce correctamente el contenido sin dejar de cumplir con la actividad.

#### Propuesta de la IA

La IA realizó una revisión global del backlog y detectó que la cantidad de texto no se debía únicamente al número de historias. También encontró que la `US-09` estaba duplicada y que varias reglas se comprobaban repetidamente mediante escenarios separados.

Entre las principales repeticiones se encontraban:

- La indicación de no modificar el historial.
- La separación de escenarios equivalentes para temperatura y humedad.
- La conservación de alertas consolidadas.
- Las consultas sobre archivos inexistentes o sin información.
- Las combinaciones individuales de filtros.
- La comprobación repetida de reglas que ya podían establecerse de manera general.

La propuesta consistió en mantener las doce historias, pero limitar cada una a un flujo principal, un caso alternativo importante y, cuando fuera necesario, un error o caso borde que modificara realmente el comportamiento.

#### Decisión tomada

Se aceptó simplificar el backlog porque la primera versión era demasiado extensa para explicarla y defenderla con claridad. No se crearon historias adicionales, ya que esto habría fragmentado nuevamente funcionalidades que pertenecían al mismo objetivo.

Se decidió conservar los casos borde que sí afectan el funcionamiento, como los datos inválidos, valores iguales al umbral, sensores inexistentes, registros dañados, filtros incorrectos, sensores que recuperan la comunicación y errores de almacenamiento o exportación.

#### Cambios realizados

- Se eliminó la copia duplicada de la `US-09`.
- Se redujo el backlog de 802 a 341 líneas.
- Se pasó de 80 a 31 escenarios.
- Se conservaron las doce historias de usuario.
- Se agruparon comportamientos equivalentes en escenarios más generales.
- Se trasladaron las decisiones transversales a una sección de reglas generales.
- Se eliminaron comprobaciones repetidas que no aportaban un comportamiento diferente.
- Se mantuvieron los escenarios necesarios para verificar los flujos principales y los errores relevantes.

#### Justificación

La primera versión era verificable, pero estaba sobredocumentada y se aproximaba más a una especificación técnica exhaustiva que a un backlog académico. Esto dificultaba su lectura y podía provocar que su contenido fuera complicado de explicar.

La versión revisada conserva el alcance funcional y los casos importantes, pero utiliza una redacción más concreta y natural. La IA ayudó a localizar las redundancias, mientras que la decisión de reducir el contenido surgió de una revisión crítica del resultado y de la necesidad de presentar un trabajo que pudiera comprenderse y defenderse personalmente.

### Entrada: Desarrollo de `SensorRegistry` mediante TDD

#### Objetivo

Desarrollar la funcionalidad correspondiente a la historia de usuario `US-01`, relacionada con el registro y la consulta de sensores. El trabajo debía realizarse mediante ciclos pequeños de desarrollo dirigido por pruebas, siguiendo la secuencia RED, GREEN y REFACTOR.

#### Herramienta utilizada

Codex.

#### Prompts utilizados

> Guíame paso a paso para implementar `SensorRegistry` mediante TDD, realizando primero la prueba RED y después la implementación mínima en GREEN.

> ¿Cómo quedaría todo el código de momento?

> Explica todo el código paso a paso.

> Quiero realizar un refactor que quede registrado correctamente en el historial de commits.

#### Propuesta de la IA

Codex propuso dividir la historia de usuario en comportamientos pequeños que pudieran desarrollarse y comprobarse individualmente:

1. Generar un error al consultar un sensor inexistente.
2. Registrar un sensor y recuperarlo mediante su identificador.
3. Rechazar identificadores duplicados.
4. Rechazar identificadores vacíos.
5. Rechazar identificadores formados únicamente por espacios.

Para cada comportamiento se creó primero una prueba que fallaba, representando la fase RED. Después se agregó únicamente el código necesario para que la prueba pasara, correspondiente a la fase GREEN.

Finalmente, Codex propuso refactorizar el método `register()` separando sus validaciones en los métodos auxiliares `_validate_sensor_id()` y `_ensure_not_registered()`. Esta reorganización permitió que el método principal expresara con mayor claridad el proceso de validar, comprobar duplicados y registrar el sensor.

#### Decisión tomada

Se decidió conservar los cinco comportamientos propuestos porque todos se relacionan directamente con la responsabilidad de registrar sensores de forma válida.

También se aceptó el refactor porque no añadió nuevas funcionalidades ni modificó los resultados de las pruebas. Su propósito fue mejorar la organización y legibilidad del código.

Durante el desarrollo fue necesario corregir el orden de los últimos commits, ya que inicialmente el cambio que rechazaba identificadores con espacios había quedado incluido dentro del commit de refactor. Como los commits todavía no se habían publicado, se retiró únicamente el último commit conservando los cambios locales. Después se registraron por separado el GREEN y el REFACTOR.

#### Cambios realizados

Se creó la excepción personalizada `SensorNotFoundError`, utilizada cuando se intenta consultar un sensor que no está registrado.

La clase `SensorRegistry` utiliza un conjunto de cadenas para almacenar identificadores sin permitir elementos repetidos. Su método `register()` valida el identificador, comprueba que no exista previamente y finalmente lo agrega al registro. El método `get()` devuelve el identificador cuando existe o genera `SensorNotFoundError` cuando no se encuentra.

Se desarrollaron cinco pruebas para comprobar el comportamiento del registro. Todas fueron creadas de manera incremental y actualmente pasan correctamente.

El historial final conserva la evidencia del ciclo RED y GREEN de cada comportamiento, seguido por un commit de REFACTOR para la reorganización de las validaciones.

#### Justificación

La IA se utilizó como apoyo para dividir la historia de usuario, proponer las pruebas, explicar los errores obtenidos y mantener el orden del proceso TDD. Las propuestas no se incorporaron de manera automática: cada prueba se ejecutó y su resultado se revisó antes de continuar.

Además, se solicitó una explicación completa de la implementación para comprender el funcionamiento del conjunto, las excepciones, los métodos auxiliares, las anotaciones de tipo y las pruebas con `pytest`. Esto permitió verificar que el resultado respondiera a la historia de usuario y que el refactor modificara únicamente la estructura interna.

### Configuración de la Definition of Done y calidad automatizada

#### Objetivo

Establecer los criterios que debe cumplir una historia de usuario para considerarse terminada y configurar las comprobaciones automáticas de calidad solicitadas para la Semana 2.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Necesito realizar la actividad del jueves de la Semana 2. Ayúdame a crear una Definition of Done para el proyecto, configurar las herramientas de calidad automatizada y aplicar correctamente el flujo de ramas y Pull Requests. Explícame cada paso para comprender qué estamos haciendo y cómo se relaciona con Scrum.

#### Propuesta de la IA

La IA propuso crear el archivo `semana2/DEFINITION_OF_DONE.md` con criterios funcionales, prácticas de TDD, comprobaciones de calidad, documentación, revisión y control de versiones. También sugirió centralizar la configuración del proyecto mediante `pyproject.toml`, estableciendo una cobertura mínima del 80 %, reglas de análisis para el código y la exigencia de anotaciones de tipo.

Durante la comprobación del proyecto, la IA ayudó a interpretar un error provocado porque Mypy reconocía `sensor_registry.py` con dos nombres de módulo diferentes. Antes de proponer una modificación, solicitó revisar la estructura del directorio y los imports utilizados en las pruebas. Con esa información se determinó que no era necesario agregar un archivo `__init__.py` y que la solución adecuada era configurar `explicit_package_bases = true`.

También se propuso realizar el trabajo en la rama `chore/calidad-automatizada-semana2`, revisar los cambios antes de confirmarlos y utilizar posteriormente un Pull Request como espacio de auto-revisión antes de fusionar la rama con `main`.

#### Decisión tomada

Se aceptó la estructura propuesta para la Definition of Done porque reúne los requisitos de la actividad y establece criterios claros para determinar cuándo una historia puede pasar a `Done`.

También se aceptó utilizar `pyproject.toml` para centralizar las comprobaciones automáticas. La corrección propuesta para Mypy se aplicó después de revisar la estructura real del proyecto y confirmar que era compatible con la forma en que se importan los módulos.

Las recomendaciones no se aplicaron automáticamente: cada archivo, comando y resultado se revisó para comprender su finalidad antes de continuar.

#### Cambios realizados

- Se creó `semana2/DEFINITION_OF_DONE.md`.
- Se creó y configuró `pyproject.toml`.
- Se estableció una cobertura mínima del 80 %.
- Se configuraron las reglas de calidad requeridas para el proyecto.
- Se activó la comprobación de anotaciones de tipo.
- Se agregó `explicit_package_bases = true` para evitar la identificación duplicada de módulos.
- Se ejecutaron cinco pruebas, todas aprobadas.
- Se obtuvo una cobertura total del 100 %.
- Se comprobó que el análisis de estilo y tipado terminara sin errores.
- Se revisó el `diff` antes de crear el commit.
- Se registraron los cambios en una rama independiente.

#### Justificación

La IA se utilizó como apoyo para interpretar los requisitos, proponer una configuración inicial y diagnosticar el problema encontrado durante las comprobaciones. La revisión de la estructura, los imports y los resultados permitió comprender las propuestas antes de incorporarlas.

La Definition of Done documenta el nivel de calidad que deberán cumplir las siguientes historias, mientras que la configuración automatizada permite verificar objetivamente parte de esos criterios. Esto evita considerar terminada una funcionalidad únicamente porque el código parece funcionar.

### Revisión del backlog y planeación del Sprint 1

#### Objetivo

Revisar la calidad de las 12 historias de usuario existentes y formalizar la planeación del Sprint 1 de acuerdo con la rúbrica. La planeación debía incluir un Sprint Goal, entre cinco y siete historias justificadas, tareas con duración máxima de cuatro horas y la Definition of Done aplicable.

#### Herramienta utilizada

- ChatGPT Codex.

#### Prompt utilizado

> Ya contamos con 12 historias de usuario en `semana2/backlog.md`. Todas tienen prioridad MoSCoW y Story Points. La `US-01` está terminada, la `US-02` a la `US-07` están en Sprint y la `US-08` a la `US-12` permanecen en Backlog. Revisa su calidad conforme a la rúbrica y ayúdame a definir el Sprint Goal, justificar la selección de siete historias y dividirlas en tareas de máximo cuatro horas, sin saltarnos el proceso ni crear trabajo innecesario.

#### Propuesta de la IA

La IA revisó las 12 historias y determinó que el Product Backlog ya superaba el mínimo solicitado. También comprobó que las historias contenían rol, necesidad, valor, escenarios Gherkin, prioridad MoSCoW y Story Points.

Se propuso conservar como selección del Sprint 1 las historias `US-01` a `US-07`, que suman 27 Story Points y forman el siguiente flujo funcional:

1. Registrar un sensor.
2. Recibir una lectura.
3. Validar sus datos.
4. Configurar los umbrales.
5. Detectar anomalías.
6. Generar una alerta.
7. Mostrarla y almacenarla.

También se propuso crear `semana2/eval1/SPRINT_PLANNING.md` con el Sprint Goal, la selección justificada, el estado de cada historia, la descomposición en tareas y la referencia a la Definition of Done.

#### Decisión tomada

Se aceptó la revisión de calidad y la estructura propuesta para la planeación porque correspondían con el contenido real de `backlog.md` y con los requisitos de la rúbrica.

Se rechazó crear historias adicionales, ya que el backlog ya contenía 12 historias completas. También se descartó mover la `US-08` al Sprint para reemplazar la `US-01`, porque una historia terminada continúa formando parte de la selección original del Sprint. Por ello, la `US-01` permanece contabilizada como `Done`, mientras que la `US-02` a la `US-07` representan el trabajo pendiente.

La planeación fue revisada antes de aprobarse para comprobar que las siete historias sumaran 27 Story Points, que todas fueran prioridad Must y que ninguna tarea individual superara las cuatro horas.

#### Cambios realizados

- Se revisaron las 12 historias existentes en `semana2/backlog.md`.
- Se confirmó que no era necesario crear historias adicionales.
- Se conservaron `US-01` a `US-07` como selección del Sprint 1.
- Se mantuvieron `US-08` a `US-12` en el Product Backlog.
- Se redactó un Sprint Goal relacionado con el núcleo del sistema de monitoreo.
- Se justificó la selección de las siete historias.
- Se dividieron las historias en tareas estimadas de máximo cuatro horas.
- Se documentó que la `US-01` está terminada y que las demás historias seleccionadas permanecen pendientes.
- Se creó `semana2/eval1/SPRINT_PLANNING.md`.
- No se realizaron cambios en el código fuente.

#### Justificación

La IA permitió contrastar el backlog existente con la rúbrica e identificar que parte del trabajo solicitado ya había sido adelantado. La propuesta no se aceptó automáticamente: se compararon las historias, sus prioridades, sus estimaciones y su estado en el tablero antes de aprobar la planeación.

Conservar la selección original evita modificar artificialmente el alcance del Sprint después de haber completado una historia. La descomposición en tareas permite visualizar el trabajo pendiente y cumplir el límite de cuatro horas establecido por la actividad.

### Desarrollo mediante TDD del registro de lecturas

#### Objetivo

Implementar la historia `US-02` para registrar lecturas de temperatura y humedad únicamente cuando el sensor exista. También se debía conservar el historial de lecturas y asignar automáticamente la fecha y hora de recepción, mostrando evidencia del ciclo RED → GREEN → REFACTOR.

#### Herramientas utilizadas

- ChatGPT Codex.
- GitHub Copilot.

#### Prompts utilizados

Para preparar las pruebas y la implementación:

> Ayúdame a desarrollar la `US-02` mediante TDD. Necesito registrar lecturas de temperatura y humedad, asociarlas con un sensor existente, conservar las lecturas anteriores y rechazar sensores inexistentes. Las validaciones de los valores pertenecen a la `US-03` y todavía no deben implementarse.

Para corregir el aviso en el archivo de pruebas:

> Corrige el problema de orden en las importaciones de este archivo.

#### Propuesta de la IA

Codex propuso crear tres pruebas automatizadas antes de realizar la implementación:

1. Registrar una lectura asociada con un sensor existente y asignarle la fecha y hora de recepción.
2. Conservar las lecturas anteriores cuando se registren nuevos datos.
3. Rechazar una lectura perteneciente a un sensor inexistente sin almacenarla.

Durante la fase RED, las pruebas fallaron porque todavía no existía el módulo `semana2.eval1.readings`.

Para alcanzar GREEN, se propusieron las clases `SensorReading` y `ReadingRecorder`. La primera representa los datos de una lectura, mientras que la segunda comprueba la existencia del sensor, obtiene la fecha mediante un reloj inyectado y conserva las lecturas registradas.

Posteriormente, Ruff detectó un problema en la organización de las importaciones del archivo de pruebas. Copilot propuso reorganizarlas utilizando el formato recomendado por la herramienta, sin modificar el comportamiento de las pruebas.

#### Decisión tomada

Se aceptaron las tres pruebas porque representan los comportamientos solicitados por la `US-02`. También se aceptó la implementación mínima propuesta para GREEN, después de revisar que reutilizara `SensorRegistry` y que no incorporara las validaciones reservadas para la `US-03`.

La reorganización de las importaciones propuesta por Copilot se aceptó únicamente después de comprobarla nuevamente con Ruff, Mypy y Pytest.

No se agregaron validaciones de temperatura, humedad ni datos incompletos, debido a que esas reglas corresponden a la siguiente historia de usuario.

#### Cambios realizados

- Se creó `semana2/eval1/tests/test_sensor_reading.py`.
- Se agregaron tres pruebas automatizadas para la `US-02`.
- Se comprobó la fase RED mediante el error causado por la ausencia de `semana2.eval1.readings`.
- Se creó `semana2/eval1/readings.py`.
- Se implementó `SensorReading` como una estructura de datos inmutable.
- Se implementó `ReadingRecorder` para registrar y conservar lecturas.
- Se reutilizó `SensorRegistry` para comprobar la existencia de los sensores.
- Se inyectó un reloj para controlar la fecha y hora durante las pruebas.
- Se reorganizaron las importaciones del archivo de pruebas para corregir el aviso de Ruff.
- Las tres pruebas de la historia terminaron correctamente.
- La ejecución completa de Semana 2 terminó con ocho pruebas aprobadas.
- Ruff y Mypy finalizaron sin errores.

#### Justificación

La IA se utilizó como apoyo para convertir los criterios de aceptación de la historia en pruebas automatizadas y para proponer una implementación mínima. El código no se aceptó automáticamente: se verificó que cada prueba correspondiera con la `US-02`, se ejecutó primero la fase RED y se comprobó que GREEN no afectara la funcionalidad anterior.

La propuesta de Copilot únicamente modificó la organización de las importaciones. Su validez se confirmó mediante las herramientas de calidad y la ejecución completa de las pruebas. De esta manera, se conservó el comportamiento del sistema y se dejó evidencia del ciclo RED → GREEN → REFACTOR.

### Desarrollo de US-03 mediante TDD

#### Objetivo

Desarrollar la validación de lecturas de sensores mediante el ciclo TDD: RED, GREEN y REFACTOR. La implementación debía rechazar datos incompletos, valores no numéricos y humedades fuera del intervalo de `0` a `100`, evitando que las lecturas inválidas fueran almacenadas.

#### Herramientas utilizadas

ChatGPT y Codex.

#### Prompt utilizado

> Ayúdame a desarrollar US-03 mediante TDD. Primero necesito crear pruebas que comprueben el rechazo de datos incompletos, valores no numéricos y humedades fuera del intervalo de 0 a 100. Después, propón la implementación mínima para aprobarlas y revisa si existe un refactor que mejore el código sin cambiar su comportamiento.

#### Propuesta de la IA

La IA propuso desarrollar la historia mediante las tres fases de TDD:

**RED:** se agregaron pruebas en `test_sensor_reading.py` para comprobar:

- Temperatura o humedad ausentes.
- Temperatura o humedad no numéricas.
- Humedad menor que `0` o mayor que `100`.
- Aceptación de los límites `0` y `100`.
- Ausencia de lecturas almacenadas después de un intento inválido.

Las pruebas esperaban una excepción llamada `InvalidReadingError`. Al ejecutarlas por primera vez, fallaron porque dicha excepción todavía no existía, confirmando correctamente la fase RED.

**GREEN:** se propuso implementar en `readings.py` la excepción `InvalidReadingError` y el método `_validate_values()`. La validación comprueba que la temperatura y la humedad sean valores numéricos, rechaza explícitamente los booleanos y verifica que la humedad se encuentre entre `0` y `100`. Esta validación se ejecuta antes de almacenar la lectura.

Con la implementación mínima, las diez pruebas de `test_sensor_reading.py` y las quince pruebas de la Semana 2 finalizaron correctamente.

**REFACTOR:** Codex identificó que la comprobación del tipo numérico estaba repetida para la temperatura y la humedad. Por ello, propuso extraerla al método `_require_numeric()` y reutilizarla desde `_validate_values()`.

Durante la revisión también se confirmó que el import correcto era:

`from semana2.sensor_registry import SensorRegistry`

debido a la ubicación real de `sensor_registry.py` dentro del proyecto.

#### Decisión tomada

Acepté las pruebas propuestas porque representaban directamente los criterios de aceptación de `US-03`. También acepté la implementación mínima para alcanzar GREEN y el refactor que eliminaba la comprobación numérica repetida.

La propuesta de la IA fue revisada antes de aplicarse. Se conservaron únicamente `_require_numeric()`, la simplificación de `_validate_values()` y el import correspondiente a la estructura real del proyecto. Se descartaron modificaciones adicionales relacionadas con el constructor y un reloj predeterminado porque no formaban parte de `US-03`.

#### Cambios realizados

Se realizaron los siguientes cambios:

- Se agregaron pruebas para valores incompletos, no numéricos y humedades fuera del intervalo permitido.
- Se creó la excepción `InvalidReadingError`.
- Se incorporó la validación antes del almacenamiento de cada lectura.
- Se comprobó que las lecturas inválidas no modificaran el estado del registrador.
- Se creó `_require_numeric()` para centralizar la validación de valores numéricos.
- Se simplificó `_validate_values()` sin modificar el comportamiento aprobado durante GREEN.
- Se mantuvo el import de `SensorRegistry` de acuerdo con la estructura real del proyecto.

Al finalizar, las quince pruebas de la Semana 2 continuaron pasando y las comprobaciones de Ruff y Mypy no presentaron errores.

#### Justificación

El uso de TDD permitió definir primero el comportamiento esperado, implementar solamente lo necesario y mejorar posteriormente la estructura interna sin alterar los resultados. La propuesta de la IA no se incorporó automáticamente: se revisaron las pruebas, el código y el diff para mantener el alcance limitado a `US-03`.

### Entrada — Desarrollo de US-04 mediante TDD

#### Objetivo

Desarrollar la configuración de los umbrales máximos de temperatura y humedad mediante el ciclo TDD: RED, GREEN y REFACTOR. El sistema debía utilizar valores predeterminados de `35 °C` y `80 %`, permitir su actualización con valores válidos y conservar la configuración anterior cuando se intentaran guardar datos inválidos.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a desarrollar US-04 mediante TDD. Necesito crear primero las pruebas para los umbrales predeterminados, la configuración de valores personalizados y el rechazo de valores no numéricos o humedades fuera del intervalo de 0 a 100. Después, propón la implementación mínima y un refactor que mejore el código sin modificar su comportamiento.

#### Propuesta de la IA

La IA propuso desarrollar la historia de usuario siguiendo las tres fases de TDD:

**RED:** se creó `test_anomaly_thresholds.py` con pruebas para comprobar:

- El uso de los umbrales predeterminados de `35 °C` y `80 %`.
- La actualización de los umbrales mediante valores personalizados válidos.
- El rechazo de temperaturas y humedades no numéricas.
- El rechazo de humedades menores que `0` o mayores que `100`.
- La aceptación de los valores límite `0` y `100`.
- La conservación de los umbrales anteriores después de una configuración inválida.

Las pruebas esperaban la existencia de `AnomalyThresholds` y `InvalidThresholdError`. La primera ejecución produjo un error porque el módulo `anomaly_thresholds.py` todavía no existía, lo cual confirmó correctamente la fase RED.

**GREEN:** se propuso crear `anomaly_thresholds.py` con una clase que inicializara los umbrales predeterminados y proporcionara el método `update()`. La implementación validó primero todos los datos y solamente sustituyó los umbrales cuando ambos valores eran válidos. También rechazó explícitamente los valores booleanos, debido a que Python los considera una subclase de `int`.

Después de implementar el comportamiento mínimo, las ocho pruebas de `US-04` y las veintitrés pruebas de la Semana 2 finalizaron correctamente.

**REFACTOR:** la IA identificó que la validación numérica estaba repetida para la temperatura y la humedad. Como mejora, propuso extraerla al método privado `_require_numeric()`, que recibe el valor y el nombre del umbral para generar el mensaje de error correspondiente.

#### Decisión tomada

Acepté las pruebas propuestas porque representaban directamente los criterios de aceptación de `US-04`. No se agregaron límites para la temperatura, ya que la historia de usuario solamente solicita rechazar valores no numéricos y restringir la humedad al intervalo de `0` a `100`.

También acepté la implementación mínima de GREEN y el refactor de la validación numérica. Antes de registrar cada cambio, comprobé que las fases RED, GREEN y REFACTOR permanecieran separadas en commits distintos.

#### Cambios realizados

Se realizaron los siguientes cambios:

- Se creó `test_anomaly_thresholds.py` con las pruebas correspondientes a los criterios de aceptación.
- Se creó la excepción `InvalidThresholdError`.
- Se implementaron los umbrales predeterminados de `35 °C` y `80 %`.
- Se agregó el método `update()` para guardar configuraciones personalizadas.
- Se validaron los valores antes de modificar los umbrales vigentes.
- Se rechazaron datos no numéricos, valores booleanos y humedades fuera del intervalo permitido.
- Se garantizó la conservación de los valores anteriores cuando la configuración fuera inválida.
- Se extrajo `_require_numeric()` para eliminar la duplicación de la validación numérica.

Al finalizar, las veintitrés pruebas de la Semana 2 continuaron pasando y las comprobaciones realizadas con Ruff y Mypy no presentaron errores.

#### Justificación

El uso de TDD permitió definir el comportamiento esperado antes de crear la implementación. La fase GREEN incorporó solamente lo necesario para satisfacer los criterios de aceptación, mientras que REFACTOR redujo la duplicación sin cambiar los resultados. Las propuestas de la IA fueron revisadas antes de aplicarse para mantener el desarrollo dentro del alcance de `US-04`.

### Entrada — Desarrollo de US-05 mediante TDD

#### Objetivo

Desarrollar la detección de condiciones ambientales anómalas mediante el ciclo TDD: RED, GREEN y REFACTOR. El sistema debía comparar cada lectura con los umbrales vigentes, identificar si la temperatura, la humedad o ambas variables superaban sus límites y conservar los valores analizados junto con los umbrales utilizados.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a desarrollar US-05 mediante TDD. Necesito crear primero las pruebas para detectar cuándo la temperatura, la humedad o ambas variables superan sus umbrales. El resultado debe conservar los valores analizados y los umbrales utilizados. Después, propón la implementación mínima y un refactor que reduzca la duplicación sin cambiar el comportamiento.

#### Propuesta de la IA

La IA propuso desarrollar la historia mediante las fases RED, GREEN y REFACTOR.

**RED:** se creó `test_anomaly_detector.py` con pruebas para comprobar:

- La detección de una temperatura superior a su umbral.
- La detección de una humedad superior a su umbral.
- La detección simultánea de ambas variables.
- La conservación del valor analizado y del umbral utilizado.
- La ausencia de anomalías cuando los valores fueran iguales o inferiores a sus límites.

Las pruebas esperaban la existencia de `AnomalyDetector`. La primera ejecución produjo un error porque `anomaly_detector.py` todavía no existía, lo cual confirmó correctamente la fase RED.

**GREEN:** se propuso crear `anomaly_detector.py` con las clases inmutables `Anomaly` y `AnalysisResult`. También se implementó `AnomalyDetector`, que recibe los umbrales vigentes y analiza objetos `SensorReading`.

La implementación comparó cada valor mediante el operador `>`, por lo que un valor igual al umbral no se considera anómalo. El detector podía devolver ninguna, una o dos anomalías, conservando en cada una el nombre de la variable, el valor recibido y el límite utilizado.

Después de implementar el comportamiento mínimo, las seis pruebas de `US-05` y las veintinueve pruebas de la Semana 2 finalizaron correctamente.

**REFACTOR:** la IA identificó duplicación en la comparación de las variables y en la construcción de los objetos `Anomaly`. Se extrajo el método privado `_detect_anomaly()` y se organizaron los datos de temperatura y humedad en una colección recorrida mediante un ciclo.

#### Decisión tomada

Acepté las pruebas porque representaban directamente los criterios de aceptación de `US-05`. Se mantuvo una comparación estricta mediante `>`, ya que los valores iguales o inferiores al umbral no deben producir anomalías.

También acepté representar cada anomalía mediante un objeto inmutable que conserva la variable, el valor analizado y el umbral utilizado. Antes del commit de REFACTOR se revisó nuevamente la propuesta para evitar una solución indirecta basada en valores opcionales y recorridos adicionales.

#### Cambios realizados

Se realizaron los siguientes cambios:

- Se creó `test_anomaly_detector.py` con las pruebas de los criterios de aceptación.
- Se creó la clase inmutable `Anomaly`.
- Se creó la clase inmutable `AnalysisResult`.
- Se implementó `AnomalyDetector`.
- Se permitió detectar anomalías de temperatura y humedad de forma independiente.
- Se permitió detectar ambas anomalías en una misma lectura.
- Se conservaron los valores analizados y los umbrales utilizados.
- Se estableció que los valores iguales o inferiores al umbral no son anómalos.
- Se extrajo `_detect_anomaly()` para centralizar la comparación y construcción de anomalías.
- Se organizó el análisis mediante un único ciclo para reducir la duplicación.

Al finalizar, las veintinueve pruebas de la Semana 2 continuaron pasando y las comprobaciones con Ruff y Mypy no presentaron errores.

#### Justificación

El ciclo TDD permitió establecer el comportamiento esperado antes de implementar el detector. La fase GREEN incorporó únicamente los elementos necesarios para satisfacer los criterios de aceptación. Posteriormente, REFACTOR redujo la duplicación y mantuvo una estructura clara sin modificar los resultados. Las propuestas de la IA fueron revisadas y ajustadas antes de aplicarse.

### Entrada — Desarrollo de US-06 mediante TDD

#### Objetivo

Desarrollar la generación de alertas para las lecturas que contienen condiciones ambientales anómalas mediante el ciclo TDD: RED, GREEN y REFACTOR. Cada alerta debía conservar el identificador del sensor, la fecha y hora de la lectura, así como los valores anómalos y sus respectivos umbrales. Cuando ambas variables fueran anómalas, debían agruparse en una sola alerta.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a desarrollar US-06 mediante TDD. Necesito generar una sola alerta por cada lectura anómala. La alerta debe incluir el identificador del sensor, la fecha y hora de la lectura, además de los valores anómalos y sus umbrales. Si la temperatura y la humedad son anómalas, deben aparecer juntas. Si no existen anomalías, no debe generarse ninguna alerta.

#### Propuesta de la IA

La IA propuso desarrollar la historia mediante las fases RED, GREEN y REFACTOR.

**RED:** se creó `test_anomaly_alerts.py` con pruebas para comprobar:

- La generación de una alerta cuando la temperatura fuera anómala.
- La generación de una alerta cuando la humedad fuera anómala.
- La conservación del identificador del sensor y la fecha y hora de la lectura.
- La agrupación de ambas anomalías en una sola alerta.
- La ausencia de una alerta cuando el análisis no contuviera anomalías.
- La conservación de los valores anómalos y sus umbrales mediante los objetos `Anomaly`.

Las pruebas esperaban la existencia de `AlertGenerator`. La primera ejecución produjo un error porque `anomaly_alerts.py` todavía no existía, lo cual confirmó correctamente la fase RED.

**GREEN:** se propuso crear `anomaly_alerts.py` con la clase inmutable `AnomalyAlert` y la clase `AlertGenerator`.

La implementación mínima utilizó el método `create()`, que recibe una lectura y su resultado de análisis. Cuando el análisis no contiene anomalías, devuelve `None`. En caso contrario, crea una sola alerta con el identificador del sensor, la fecha y hora de recepción y todas las anomalías encontradas.

Después de implementar el comportamiento mínimo, las cinco pruebas de `US-06` y las treinta y cuatro pruebas de la Semana 2 finalizaron correctamente.

**REFACTOR:** la IA observó que `AlertGenerator` no conserva estado ni utiliza atributos de instancia. Por esta razón, propuso convertir `create()` en un método estático mediante `@staticmethod`. También se actualizaron las pruebas para mantenerlas alineadas con esta forma de invocar el generador.

#### Decisión tomada

Acepté las pruebas propuestas porque representan directamente los criterios de aceptación de `US-06`. También acepté utilizar un objeto inmutable para representar la alerta, ya que sus datos corresponden a una lectura que ya fue recibida y analizada.

La implementación devuelve `None` cuando no existen anomalías para expresar claramente que no debe generarse una alerta. Cuando existen una o dos anomalías, ambas se conservan dentro de un único objeto `AnomalyAlert`.

Acepté el refactor del método estático porque la generación de la alerta no depende del estado interno de `AlertGenerator`. El cambio se realizó después de comprobar el funcionamiento de la implementación GREEN.

#### Cambios realizados

Se realizaron los siguientes cambios:

- Se creó `test_anomaly_alerts.py` con las pruebas de los criterios de aceptación.
- Se creó la clase inmutable `AnomalyAlert`.
- Se implementó `AlertGenerator`.
- Se agregó el método `create()` para generar alertas.
- Se conservó el identificador del sensor.
- Se conservó la fecha y hora de la lectura.
- Se conservaron los valores anómalos y sus respectivos umbrales.
- Se agruparon las anomalías de temperatura y humedad en una sola alerta.
- Se estableció que una lectura sin anomalías no produce una alerta.
- Se convirtió `create()` en un método estático.
- Se actualizaron las pruebas para reflejar el refactor realizado.

Al finalizar, las treinta y cuatro pruebas de la Semana 2 continuaron pasando y las comprobaciones con Ruff y Mypy no presentaron errores.

#### Justificación

El ciclo TDD permitió establecer el comportamiento esperado antes de implementar la generación de alertas. La fase GREEN incorporó únicamente los elementos necesarios para satisfacer los criterios de aceptación. Posteriormente, REFACTOR expresó con mayor claridad que la generación de alertas no depende de un estado interno, sin modificar los resultados obtenidos. Las propuestas realizadas por la IA fueron revisadas antes de incorporarlas al proyecto.

### Entrada — Desarrollo de US-07 mediante TDD

#### Objetivo

Desarrollar la publicación de alertas mediante el ciclo TDD: RED, GREEN y REFACTOR. Cada alerta debía mostrarse en consola y almacenarse en un archivo JSON Lines. Los nuevos registros debían agregarse sin eliminar los anteriores y, si ocurría un error durante la escritura, la alerta todavía debía mostrarse y el problema debía informarse claramente.

#### Herramienta utilizada

ChatGPT.

#### Prompt utilizado

> Ayúdame a desarrollar US-07 mediante TDD. Necesito mostrar cada alerta en consola y almacenarla en formato JSON Lines. El archivo debe crearse si no existe y las nuevas alertas deben agregarse sin borrar las anteriores. Si el almacenamiento falla, la alerta debe seguir apareciendo en consola y se debe informar claramente el error de escritura.

#### Propuesta de la IA

La IA propuso desarrollar la historia mediante las fases RED, GREEN y REFACTOR.

**RED:** se creó `test_alert_publisher.py` con pruebas para comprobar:

- La presentación de la alerta en consola como un objeto JSON.
- La creación del archivo JSON Lines cuando todavía no existe.
- El almacenamiento de un registro equivalente a la alerta.
- La escritura de cada alerta en una línea independiente.
- La conservación de registros anteriores al publicar nuevas alertas.
- La presentación de la alerta incluso cuando ocurre un error de almacenamiento.
- La notificación del error de escritura mediante la salida de error.

Las pruebas esperaban la existencia de `AlertPublisher`. La primera ejecución produjo un error porque `alert_publisher.py` todavía no existía, lo cual confirmó correctamente la fase RED.

**GREEN:** se propuso crear `alert_publisher.py` con la clase `AlertPublisher`.

La implementación mínima convirtió cada objeto `AnomalyAlert` en un registro serializable con el identificador del sensor, la fecha y hora de la lectura y la colección de anomalías. Posteriormente, el registro se transformó a JSON, se mostró en consola y se escribió en el archivo configurado.

El archivo se abrió en modo de adición mediante `"a"`, permitiendo crearlo cuando no existía y agregar alertas sin eliminar los registros anteriores. Los errores derivados de la escritura se capturaron mediante `OSError` y se informaron por la salida de error sin impedir la presentación de la alerta en consola.

Después de implementar el comportamiento mínimo, las cuatro pruebas de `US-07` y las treinta y ocho pruebas de la Semana 2 finalizaron correctamente.

**REFACTOR:** la IA propuso separar las operaciones internas de `AlertPublisher` para evitar que `publish()` concentrara toda la lógica.

Se extrajo el método estático `_serialize()`, responsable de convertir la alerta en una cadena JSON, y el método `_append_to_file()`, encargado exclusivamente de agregar el registro al archivo. De esta manera, `publish()` quedó como el método que coordina la presentación, el almacenamiento y el manejo de errores.

Durante el cierre del refactor aparecieron modificaciones locales adicionales en archivos que no correspondían a `US-07`. Antes de crear otro commit, se revisó el estado del repositorio y se restauraron selectivamente únicamente esos cambios accidentales, sin modificar ni repetir los commits ya registrados.

#### Decisión tomada

Acepté las pruebas propuestas porque representan los criterios de aceptación de `US-07`. Se eligió el formato JSON Lines porque permite almacenar cada alerta como un objeto JSON independiente y agregar nuevos registros sin reescribir el contenido existente.

También acepté que la alerta se muestre antes de intentar almacenarla. Esta decisión garantiza que la información permanezca visible en consola aunque falle la escritura del archivo.

El refactor fue aceptado porque separa la serialización y el almacenamiento en métodos con responsabilidades específicas, mientras que `publish()` conserva la coordinación general del proceso. Los cambios locales ajenos a la historia no se incorporaron, ya que no formaban parte del alcance de `US-07`.

#### Cambios realizados

Se realizaron los siguientes cambios:

- Se creó `test_alert_publisher.py` con las pruebas de los criterios de aceptación.
- Se creó `alert_publisher.py`.
- Se implementó la clase `AlertPublisher`.
- Se convirtió cada alerta en un registro JSON.
- Se mostró cada alerta en consola.
- Se creó automáticamente el archivo JSON Lines cuando no existía.
- Se escribió una alerta por línea.
- Se agregaron registros sin eliminar las alertas anteriores.
- Se capturaron los errores de almacenamiento mediante `OSError`.
- Se informó el error mediante la salida de error.
- Se mantuvo la presentación de la alerta aunque fallara el almacenamiento.
- Se extrajo `_serialize()` para realizar la serialización.
- Se extrajo `_append_to_file()` para realizar la escritura.
- Se restauraron selectivamente modificaciones accidentales ajenas a la historia.

Al finalizar, las treinta y ocho pruebas de la Semana 2 continuaron pasando y las comprobaciones con Ruff y Mypy no presentaron errores.

#### Justificación

El ciclo TDD permitió definir el comportamiento esperado antes de implementar el publicador. La fase GREEN incorporó únicamente las operaciones necesarias para satisfacer los criterios de aceptación. Posteriormente, REFACTOR separó la serialización, el almacenamiento y la coordinación general sin modificar el comportamiento verificado por las pruebas.

La revisión del estado de Git también permitió evitar que modificaciones accidentales de otros archivos se incorporaran al historial de `US-07`. Las propuestas de la IA fueron revisadas antes de aplicarse y solo se conservaron los cambios relacionados con la historia.

## Semana 3 — Desarrollo de una API REST con FastAPI

### Lunes — Creación de la estructura inicial y primeros endpoints de SensorHub

#### Objetivo

Crear la estructura inicial del proyecto SensorHub y desarrollar una primera versión funcional de su API REST. La actividad se realizó con base en los módulos de FastAPI estudiados durante el lunes, considerando la organización del proyecto, el uso de modelos Pydantic, la creación de endpoints y la utilización de códigos de estado HTTP.

#### Herramienta utilizada

Codex.

#### Prompt utilizado

> Revisa el repositorio actual y ayúdame a crear la estructura inicial de SensorHub con base en los contenidos estudiados en los módulos del curso de FastAPI correspondientes al lunes.
>
> Después, implementa una primera versión funcional de la API con un endpoint `GET /health` y un endpoint `POST /readings`. Utiliza modelos Pydantic para validar los datos de entrada y definir la respuesta. La lectura debe incluir un identificador de sensor, temperatura y humedad; además, el servidor debe generar la fecha y hora de recepción en UTC.
>
> Mantén la implementación sencilla y limitada al alcance de esta actividad. No agregues todavía persistencia, SQLAlchemy, CRUD completo ni una separación avanzada por capas. Al finalizar, verifica el funcionamiento mediante Ruff, mypy, Uvicorn y solicitudes reales. Explica los cambios realizados para que el código pueda ser revisado y comprendido antes de aceptarlo.

#### Propuesta de la IA

Codex ayudó a establecer la estructura inicial de SensorHub tomando como referencia la organización presentada en el curso de FastAPI. Esta estructura contempla el paquete principal `app` y directorios destinados a los modelos, esquemas, repositorios, servicios y routers que se utilizarán conforme avance el desarrollo del proyecto.

Para la actividad del lunes, Codex mantuvo la implementación principal en `app/main.py`, ya que todavía no era necesario utilizar todas las capas disponibles. En este archivo configuró una aplicación FastAPI con el título `SensorHub` y creó los modelos Pydantic `ReadingInput` y `ReadingResponse`.

También implementó el endpoint `GET /health`, utilizado para comprobar que la API se encuentra funcionando, y el endpoint `POST /readings`, encargado de recibir y validar lecturas de temperatura y humedad. La propuesta incluyó la validación de un identificador de sensor no vacío, una humedad entre 0 y 100 y la generación automática de la fecha y hora de recepción en UTC.

En `requirements.txt`, Codex agregó únicamente las dependencias directas necesarias para esta primera versión: FastAPI, Pydantic y Uvicorn.

#### Decisión tomada

Se decidió utilizar la estructura propuesta por Codex porque corresponde a la organización estudiada en los módulos del curso y permite preparar el proyecto para las siguientes actividades de la Semana 3.

La implementación no fue aceptada únicamente por haber sido generada por la IA. Antes de conservarla, se revisó el contenido de `app/main.py` y se estudió el funcionamiento de las importaciones, los modelos Pydantic, las restricciones definidas mediante `Field`, los decoradores de FastAPI, los códigos HTTP y la generación de fechas en UTC.

También se comprobó el recorrido de una solicitud enviada a `POST /readings`, desde la validación del JSON hasta la construcción de la respuesta. De esta manera, solamente se aceptó el código después de comprender su funcionamiento y verificar que respetara el alcance establecido.

#### Cambios realizados

- Se creó la estructura inicial de `app` con base en la organización estudiada en el curso de FastAPI.
- Se configuró la aplicación FastAPI con el título `SensorHub`.
- Se creó el modelo de entrada `ReadingInput`.
- Se creó el modelo de respuesta `ReadingResponse`.
- Se implementó `GET /health` con respuesta `200 OK`.
- Se implementó `POST /readings` con respuesta `201 Created`.
- Se validó que `sensor_id` no sea una cadena vacía.
- Se validó que la humedad se encuentre entre 0 y 100.
- Se generó `received_at` mediante una fecha y hora UTC.
- Se agregaron FastAPI, Pydantic y Uvicorn a `requirements.txt`.
- Se comprobó manualmente la documentación interactiva disponible en `/docs`.
- Se probó una lectura válida y se obtuvo `201 Created`.
- Se probó una humedad igual a 101 y se obtuvo `422`.
- Se ejecutaron Ruff, mypy y `git diff --check` sin encontrar errores.

#### Justificación

Codex se utilizó como apoyo para proponer la estructura inicial y transformar los conceptos estudiados en el curso de FastAPI en una implementación funcional. Su participación permitió construir y verificar la base de SensorHub, pero cada elemento generado fue revisado antes de aceptarse.

El uso de la IA no sustituyó el proceso de aprendizaje. Se analizó el código, se comprendió la función de sus componentes y se realizaron pruebas manuales para confirmar su comportamiento. La implementación se mantuvo sencilla porque la persistencia, SQLAlchemy y la separación completa por capas serán incorporadas gradualmente durante las siguientes actividades.

### Martes – Implementación de persistencia con SQLAlchemy 2.x

#### Objetivo

Incorporar persistencia de datos a SensorHub mediante SQLAlchemy 2.x y SQLite. La actividad consistió en configurar la conexión con la base de datos, definir el modelo ORM de una lectura, crear el esquema de manera reproducible y comprobar mediante una prueba automatizada que una lectura puede almacenarse y recuperarse correctamente.

#### Herramienta utilizada

Codex.

#### Prompt utilizado

> Ayúdame a implementar la persistencia de SensorHub con SQLAlchemy 2.x, aplicando al proyecto los conceptos estudiados durante el martes. Quiero que la configuración, el modelo ORM, la creación de las tablas y la comprobación de la persistencia queden guardados como código permanente.
>
> La implementación debe utilizar SQLite, una clase base declarativa, un `Engine` y una fábrica de sesiones. El modelo debe representar las lecturas recibidas por SensorHub e incluir el identificador del sensor, la temperatura, la humedad y la fecha de recepción.
>
> También necesito una prueba automatizada que guarde una lectura, cierre la sesión y posteriormente la recupere desde una nueva sesión. Mantén la actividad limitada a persistencia; todavía no agregues repositorios, servicios ni la integración con los endpoints de FastAPI. Revisa el código generado para evitar errores de Pylance y comprueba su funcionamiento antes de preparar el commit.

#### Propuesta de la IA

Inicialmente, Codex guio una revisión práctica del Quick Start de SQLAlchemy mediante bloques de Python ejecutados desde Bash. Con ellos se comprobaron las operaciones básicas del ORM: creación de tablas, inserción, consulta, modificación y eliminación de registros.

Después de revisar el resultado, se identificó que esas operaciones habían servido para comprender SQLAlchemy, pero la mayor parte del trabajo solamente existía como comandos temporales de terminal. Por esta razón, se decidió descartar los cambios iniciales y reiniciar la actividad desde el último commit limpio, procurando que la persistencia quedara implementada como parte permanente de SensorHub.

Codex propuso agregar SQLAlchemy 2.x a las dependencias y configurar en `app/db.py` la dirección de la base SQLite, el `Engine`, la clase declarativa `Base` y la fábrica de sesiones `SessionLocal`. La configuración incluyó las opciones necesarias para utilizar SQLite y controlar el comportamiento de las sesiones.

También propuso crear el modelo ORM `Reading` mediante el sistema de tipado de SQLAlchemy 2.x con `Mapped` y `mapped_column`. El modelo representa la tabla `readings` e incluye una clave primaria, el identificador del sensor, la temperatura, la humedad y la fecha de recepción. El identificador del sensor se definió como una columna indexada para facilitar futuras búsquedas.

Para que la creación del esquema no dependiera de instrucciones temporales, se creó `app/init_db.py`. Este módulo permite generar las tablas registradas ejecutando `python -m app.init_db`.

Finalmente, Codex propuso una prueba automatizada de persistencia. La prueba crea una base SQLite temporal, abre una sesión, almacena una lectura y confirma la transacción. Después abre una sesión diferente y recupera el registro mediante una consulta `SELECT`, verificando que todos sus valores se conservaron.

#### Decisión tomada

Se decidió conservar la estructura propuesta porque separa la configuración de la base de datos, la definición del modelo y la inicialización del esquema. Además, deja preparada una fábrica de sesiones que podrá utilizarse posteriormente desde las capas de repositorio y servicio.

No se conectó directamente el endpoint `POST /readings` con SQLAlchemy, ya que hacerlo durante esta actividad habría mezclado la lógica de FastAPI con el acceso a datos. La integración se realizará posteriormente, después de desarrollar las capas correspondientes.

Durante la implementación se revisó cada componente antes de aceptarlo. Se estudió la relación entre `Base`, `Engine`, `SessionLocal` y el modelo `Reading`, así como el recorrido de una transacción desde `session.add()` hasta `session.commit()`.

También se corrigieron dos propuestas para mantener el código limpio. En `app/init_db.py` se evitó silenciar una advertencia por importación no utilizada y se utilizó explícitamente `Reading.metadata`. En la prueba se agregó el tipo `Path` al fixture `tmp_path`, eliminando los avisos de Pylance sin recurrir a comentarios de exclusión.

#### Cambios realizados

- Se agregó `sqlalchemy==2.0.51` a `requirements.txt`.
- Se configuró `DATABASE_URL` para utilizar la base local `sensorhub.db`.
- Se creó el `Engine` de SQLAlchemy para SQLite.
- Se definió la clase declarativa `Base`.
- Se creó la fábrica de sesiones `SessionLocal`.
- Se creó el paquete `app/models`.
- Se implementó el modelo ORM `Reading`.
- Se definió la tabla `readings` con sus columnas y tipos correspondientes.
- Se configuró `sensor_id` como una columna indexada.
- Se implementó una representación legible del modelo mediante `__repr__`.
- Se creó `app/init_db.py` para inicializar el esquema de manera reproducible.
- Se agregaron los archivos locales de SQLite a `.gitignore`.
- Se generó localmente `sensorhub.db` y se comprobó que Git no la registrara.
- Se creó `tests/test_reading_persistence.py`.
- La prueba utiliza una base SQLite temporal para no modificar la base principal.
- Se comprobó que una lectura permanece almacenada después de cerrar la primera sesión.
- Se verificó la recuperación de la lectura desde una nueva sesión.
- Se corrigieron los avisos de Pylance mediante tipado y uso explícito de los elementos importados.
- Se verificaron la sintaxis, el análisis estático y el tipado de los archivos involucrados.
- La prueba aislada de persistencia finalizó correctamente con `1 passed`.

#### Justificación

Codex se utilizó como apoyo para trasladar los conceptos del Quick Start de SQLAlchemy 2.x a la estructura real de SensorHub. La primera práctica en Bash permitió comprender el funcionamiento del ORM, pero su resultado no era suficiente como implementación permanente. La revisión posterior ayudó a reconocer esta limitación y a reconstruir la actividad con archivos reutilizables y una prueba automatizada.

El uso de una base temporal en la prueba permite demostrar persistencia real sin modificar `sensorhub.db` ni dejar archivos adicionales dentro del repositorio. Abrir una segunda sesión después del `commit` confirma que el registro no solamente permanecía en la memoria de la primera sesión, sino que fue almacenado efectivamente en SQLite.

La participación de la IA no sustituyó la comprensión del proceso. Se revisaron las propuestas, se cuestionaron las decisiones que solamente silenciaban advertencias y se modificó la estructura cuando fue necesario. Como resultado, SensorHub cuenta ahora con la base de persistencia requerida para continuar posteriormente con repositorios, servicios e integración con FastAPI, sin adelantar responsabilidades correspondientes a los siguientes días.

### Miércoles – Implementación del repositorio y servicio de lecturas

#### Objetivo

Desarrollar las capas de repositorio y servicio de SensorHub para separar el acceso a la base de datos de las reglas de negocio. La actividad consistió en implementar el almacenamiento y la consulta de lecturas mediante SQLAlchemy, validar los datos antes de guardarlos y comprobar cada responsabilidad con pruebas independientes.

La implementación debía aprovechar la persistencia desarrollada el martes, pero sin conectarla todavía con los endpoints de FastAPI, ya que esa integración corresponde a una actividad posterior.

#### Herramienta utilizada

Codex.

#### Prompt utilizado

> Continuemos con la actividad del miércoles. Quiero implementar el repositorio y el servicio de lecturas utilizando la persistencia desarrollada el martes. Guíame por archivo y mantén separadas las reglas de negocio del acceso a SQLite. Todavía no conectes estas capas con los endpoints de FastAPI.
>
> Primero necesito comprobar las reglas del servicio mediante pruebas aisladas. Después quiero verificar el repositorio real con una base SQLite temporal, comprobando que una lectura permanezca almacenada y que las consultas filtren correctamente por sensor.
>
> Si durante las verificaciones aparecen errores de tipado o advertencias de Pylance, ayúdame a entender su causa y a corregirlos sin cambiar innecesariamente la lógica del programa. Antes de preparar el commit, explícame detalladamente qué función cumple cada archivo y cómo se relacionan el servicio, el repositorio, SQLAlchemy y las pruebas.

#### Propuesta de la IA

Codex propuso organizar la funcionalidad en dos capas principales. La primera sería una capa de repositorio encargada exclusivamente de comunicarse con SQLAlchemy, mientras que la segunda contendría las reglas que debe cumplir una lectura antes de ser almacenada.

Para establecer la comunicación entre ambas capas, se propuso definir `ReadingRepository` mediante un `Protocol`. Este contrato especifica que cualquier repositorio utilizado por el servicio debe ofrecer una operación para agregar lecturas y otra para consultarlas mediante el identificador del sensor.

La implementación real del contrato se realizó mediante `SQLAlchemyReadingRepository`. Esta clase recibe una sesión de SQLAlchemy desde el exterior y utiliza el modelo ORM `Reading` creado durante la actividad del martes. Su método `add()` incorpora la lectura a la sesión, confirma la transacción y actualiza el objeto para recuperar los valores generados por SQLite, principalmente la clave primaria. También incluye un `rollback()` para restaurar la sesión si la transacción no puede completarse.

Para la consulta de lecturas, Codex propuso el método `list_by_sensor()`. Este método construye una consulta con `select()`, filtra los registros cuyo `sensor_id` coincide con el solicitado y los ordena de forma ascendente mediante la fecha de recepción. El identificador de la lectura se utiliza como segundo criterio para mantener un orden estable cuando dos registros tienen la misma fecha.

La segunda parte de la propuesta fue crear `ReadingService` como responsable de las reglas de negocio. El servicio recibe un objeto que cumpla el contrato `ReadingRepository`, por lo que no depende directamente de SQLAlchemy. Antes de construir una lectura, elimina los espacios exteriores del identificador del sensor y comprueba que el resultado no esté vacío. También rechaza temperaturas inferiores al cero absoluto y humedades fuera del intervalo de `0 %` a `100 %`.

Codex también propuso inyectar una función de reloj en `ReadingService`. Durante la ejecución normal se utiliza la fecha actual en UTC, pero en las pruebas puede proporcionarse una fecha fija. Esto permite comprobar de manera exacta el valor de `received_at` y evita que las pruebas dependan de la hora real en que se ejecutan.

Para verificar las reglas del servicio de manera aislada, se utilizó un repositorio falso que almacena las lecturas en una lista de Python. Esta implementación ofrece las mismas operaciones definidas por el `Protocol`, pero no necesita SQLAlchemy ni SQLite. De esta manera, si una prueba del servicio falla, el problema puede localizarse en sus validaciones y no en la configuración de la base de datos.

Posteriormente se agregaron pruebas específicas para `SQLAlchemyReadingRepository`. Estas pruebas utilizan una base SQLite temporal proporcionada por `tmp_path`, evitando cualquier modificación en `sensorhub.db`. Una prueba guarda una lectura y abre una sesión diferente para demostrar que el registro permaneció realmente en la base de datos. La segunda guarda lecturas de distintos sensores y comprueba que la consulta devuelva solamente las correspondientes al sensor solicitado y en orden cronológico.

Durante la comprobación del tipado, Mypy detectó que la función auxiliar encargada de crear el motor de prueba no indicaba su tipo de retorno. Codex explicó que la función devolvía un objeto `Engine` y propuso agregar la importación y la anotación correspondiente. Esta corrección no modificó el comportamiento del programa; únicamente completó la información de tipos requerida por el análisis estático.

#### Decisión tomada

Se decidió conservar la separación entre servicio y repositorio porque ambos componentes atienden responsabilidades diferentes. `ReadingService` determina si los datos recibidos cumplen las reglas del sistema, mientras que `SQLAlchemyReadingRepository` se encarga de almacenarlos y recuperarlos mediante SQLAlchemy.

También se conservó `ReadingRepository` como un contrato basado en `Protocol`. Esta decisión permite que el servicio trabaje con distintas implementaciones sin conocer sus detalles internos. En la aplicación podrá utilizar el repositorio real, mientras que en las pruebas puede utilizar una versión falsa almacenada en memoria.

Se aceptó recibir la sesión de SQLAlchemy mediante el constructor del repositorio en lugar de crearla internamente. De esta forma se controla qué sesión utiliza cada instancia y se facilita su integración posterior con el sistema de dependencias de FastAPI.

En el servicio se mantuvieron las siguientes reglas:

- El identificador del sensor se normaliza eliminando espacios al principio y al final.
- Un identificador vacío se considera inválido.
- No se permiten temperaturas inferiores a `-273.15 °C`.
- La humedad debe encontrarse entre `0 %` y `100 %`, incluyendo ambos límites.
- La fecha de recepción se obtiene mediante una función de reloj inyectable.
- Las lecturas válidas se entregan al repositorio después de completar las validaciones.
- Las lecturas inválidas se rechazan antes de llegar a la capa de persistencia.

Se decidió ordenar las consultas desde la lectura más antigua hasta la más reciente porque este orden facilita la interpretación posterior del historial de cada sensor. También se mantuvo el identificador de la lectura como criterio secundario para evitar resultados ambiguos cuando varias lecturas tienen la misma fecha.

Las propuestas se comprobaron de forma progresiva. Primero se probaron las reglas del servicio con el repositorio falso y después se verificó el repositorio real con SQLite temporal. Antes de preparar el commit se solicitó una explicación completa de la arquitectura, el flujo de una lectura, el funcionamiento de las transacciones y la diferencia entre ambos tipos de pruebas.

No se modificaron todavía los endpoints de FastAPI. Integrarlos durante esta actividad habría mezclado el desarrollo de las capas internas con la exposición de la API. La conexión mediante dependencias se realizará después de comprobar que el servicio y el repositorio funcionan correctamente por separado.

#### Cambios realizados

- Se creó `app/repositories/reading_repository.py`.
- Se definió `ReadingRepository` mediante un `Protocol`.
- Se establecieron las operaciones `add()` y `list_by_sensor()`.
- Se implementó `SQLAlchemyReadingRepository`.
- El repositorio recibe una `Session` de SQLAlchemy mediante su constructor.
- Se implementó el almacenamiento de lecturas mediante `session.add()`.
- Se agregó `session.commit()` para confirmar las transacciones.
- Se utilizó `session.refresh()` para actualizar la lectura con su identificador generado.
- Se agregó `session.rollback()` para recuperar la sesión en caso de error.
- Se implementó una consulta con `select()` para filtrar lecturas por `sensor_id`.
- Los resultados se ordenan por `received_at` y, como segundo criterio, por `id`.
- Se creó `app/services/reading_service.py`.
- Se implementó `ReadingService` con inyección del repositorio.
- Se agregó una función de reloj configurable con fecha UTC.
- Se normaliza el identificador del sensor mediante `strip()`.
- Se rechazan identificadores vacíos.
- Se rechazan temperaturas inferiores al cero absoluto.
- Se validan humedades dentro del intervalo permitido.
- Se implementó la creación de objetos `Reading` después de completar las validaciones.
- Se agregó la consulta de lecturas por sensor desde el servicio.
- Se creó `tests/test_reading_service.py`.
- Se implementó `FakeReadingRepository` para probar el servicio sin SQLite.
- Se agregó un reloj fijo para obtener resultados deterministas.
- Se comprobó el almacenamiento de una lectura válida.
- Se verificó la normalización del identificador del sensor.
- Se comprobaron los casos de identificador vacío, temperatura inválida y humedad fuera de rango.
- Se verificó que las lecturas inválidas no lleguen al repositorio.
- Se comprobó la consulta de lecturas correspondientes a un sensor.
- Se creó `tests/test_reading_repository.py`.
- Se configuró una base SQLite temporal para las pruebas del repositorio.
- Se verificó que una lectura permanezca almacenada al abrir una sesión diferente.
- Se comprobó el filtrado de registros por identificador del sensor.
- Se verificó el orden cronológico de los resultados.
- Se agregó `Engine` como tipo de retorno de la función auxiliar que crea el motor de prueba.
- Se realizaron las comprobaciones de pruebas, formato y tipado de los archivos involucrados.
- Aprobaron seis casos correspondientes al servicio y dos casos correspondientes al repositorio.

#### Justificación

La separación entre servicio y repositorio evita que las validaciones del sistema queden mezcladas con consultas, sesiones y transacciones de SQLAlchemy. Esto permite modificar las reglas de negocio sin alterar el acceso a la base de datos y cambiar la implementación de persistencia sin reescribir el servicio.

El uso de `Protocol` reduce el acoplamiento porque `ReadingService` depende de las operaciones que necesita y no de una clase concreta. El repositorio falso demuestra esta ventaja, ya que puede sustituir al repositorio de SQLAlchemy durante las pruebas sin realizar cambios en el servicio.

La inyección del reloj cumple una función similar. En lugar de depender directamente de la hora del sistema, el servicio recibe una función que proporciona la fecha. Durante la ejecución normal se utiliza UTC, mientras que en las pruebas se utiliza una fecha conocida. Esto hace que los resultados sean repetibles y fáciles de comprobar.

Las pruebas del servicio y del repositorio se mantuvieron separadas porque buscan errores diferentes. Las primeras verifican la normalización, las validaciones y la delegación del almacenamiento. Las segundas comprueban que las transacciones y consultas funcionen realmente con SQLAlchemy y SQLite. La base temporal permite realizar estas comprobaciones sin modificar la base principal ni generar archivos permanentes dentro del repositorio.

Codex se utilizó para orientar la estructura, proponer fragmentos de implementación, explicar los conceptos involucrados y corregir un problema puntual de tipado. Las propuestas se integraron después de ejecutar las pruebas y revisar el funcionamiento de cada componente. La explicación solicitada antes del commit permitió comprender el recorrido completo de una lectura desde que entra al servicio hasta que es almacenada y consultada mediante el repositorio.

La participación de la IA no sustituyó la revisión ni la comprensión del proceso. Cada componente se comprobó por separado, se analizaron los resultados de las pruebas y se corrigieron los problemas encontrados antes de conservar la implementación.

Como resultado, SensorHub cuenta con una capa interna validada para administrar lecturas. Esta estructura deja preparado el proyecto para que, durante la siguiente actividad, FastAPI obtenga una sesión, construya el repositorio, inyecte el servicio y exponga estas operaciones mediante sus endpoints.

### Jueves – Integración de las capas y API REST completa

#### Objetivo

Conectar las capas internas de SensorHub con FastAPI mediante inyección de dependencias y completar las operaciones REST necesarias para administrar lecturas almacenadas en SQLite.

La actividad debía integrar los esquemas, el servicio y el repositorio sin colocar reglas de negocio ni consultas de SQLAlchemy directamente dentro de los endpoints. También debía incorporar paginación, filtros por fecha y respuestas HTTP básicas, manteniendo el desarrollo dentro del estándar esperado y sin implementar las extensiones correspondientes al nivel de alto potencial.

#### Herramienta utilizada

Codex

#### Prompt utilizado

> Continuemos con la actividad del jueves de SensorHub. Primero revisa todos los archivos existentes y confirma qué corresponde al trabajo previo y qué falta desarrollar.
>
> Guíame indicando siempre el nombre exacto del archivo que debo crear o modificar y proporciona el contenido completo. Necesito conectar FastAPI con el servicio, el repositorio y SQLite mediante inyección de dependencias.
>
> La API debe incluir las operaciones para crear, listar, consultar, actualizar y eliminar lecturas. También debe admitir paginación y filtros por fecha. Mantén el trabajo dentro del estándar esperado y no implementes extensiones de alto potencial ni un manejo exhaustivo de errores.
>
> Comprueba el funcionamiento mediante pruebas, Ruff, Mypy, SQLite y Swagger. Los commits se realizarán hasta completar toda la actividad.

#### Propuesta de la IA

La IA comenzó revisando el estado completo de la aplicación, las pruebas existentes y los cambios locales. Esta revisión permitió confirmar que la persistencia, el modelo ORM, el repositorio y el servicio desarrollados durante los días anteriores funcionaban como base para la integración.

Se propuso crear `app/dependencies.py` para administrar el ciclo de vida de las sesiones de SQLAlchemy. La función `get_session()` abre una sesión mediante `SessionLocal`, la proporciona durante la petición y permite cerrarla al finalizar. La función `get_reading_service()` utiliza la sesión para construir un `SQLAlchemyReadingRepository` y posteriormente un `ReadingService`.

También se propuso crear `app/schemas/reading.py` con tres modelos Pydantic. `ReadingCreate` representa los datos necesarios para registrar una lectura, `ReadingUpdate` permite recibir cambios parciales y `ReadingResponse` transforma los modelos ORM en respuestas de la API mediante `from_attributes=True`.

El repositorio se amplió para incorporar las operaciones necesarias para el CRUD. Además de almacenar y listar lecturas, se agregaron la consulta por identificador, la actualización y la eliminación. La consulta por sensor se extendió con `limit`, `offset`, `from_date` y `to_date`.

El servicio también fue ampliado para coordinar estas operaciones y mantener las reglas de negocio fuera del router. Se centralizó la normalización del identificador del sensor, la validación de temperatura y humedad, la comprobación de los parámetros de paginación, el orden correcto de las fechas y la validación de identificadores positivos.

Inicialmente, los endpoints HTTP se desarrollaron mediante ciclos TDD. Para cada operación se agregó primero una prueba en `tests/test_readings_api.py`. Las pruebas sustituyeron la dependencia real mediante `app.dependency_overrides`, utilizando un servicio falso para comprobar únicamente la capa HTTP.

Los resultados RED fueron `404 Not Found` cuando la ruta todavía no existía y `405 Method Not Allowed` cuando la ruta existía para otro método HTTP. Después se implementó el código mínimo necesario para obtener el GREEN.

Los endpoints incorporados fueron:

- `POST /sensors/{sensor_id}/readings`.
- `GET /sensors/{sensor_id}/readings`.
- `GET /readings/{reading_id}`.
- `PATCH /readings/{reading_id}`.
- `DELETE /readings/{reading_id}`.

Durante el refactor se creó el alias tipado `ReadingServiceDependency` para evitar repetir en cada endpoint la declaración completa de `Annotated`, `ReadingService`, `Depends` y `get_reading_service`.

Posteriormente se decidió dejar de aplicar un ciclo TDD individual para cada ajuste restante, ya que los comportamientos principales ya estaban cubiertos y era necesario aprovechar mejor el tiempo disponible. Las pruebas creadas se conservaron como protección y los cambios posteriores se realizaron mediante implementación, explicación y verificación.

La IA propuso agregar un manejo HTTP básico dentro del router. Los errores de negocio representados mediante `ValueError` se traducen a `400 Bad Request`, mientras que los resultados inexistentes se convierten en `404 Not Found`. La validación estructural de cuerpos y parámetros continúa siendo responsabilidad automática de FastAPI y Pydantic mediante respuestas `422`.

Se evitó implementar una jerarquía de excepciones de dominio, manejadores globales, conflictos `409` artificiales y pruebas exhaustivas de cada combinación de errores, porque esas características pertenecen a una extensión superior al estándar esperado.

También se revisó el uso de `PATCH`. Se decidió conservarlo porque aparece en la guía y representa correctamente una actualización parcial. El esquema `ReadingUpdate` permite enviar solamente temperatura o humedad, y el servicio modifica únicamente los campos proporcionados.

Durante las pruebas con `TestClient` apareció una advertencia de Starlette y una cascada de tipos desconocidos en Pylance. La revisión confirmó que este problema no estaba relacionado con el uso de SQLAlchemy 2.x ni con `Mapped` y `mapped_column`.

El entorno conservó `httpx`, tal como indica la guía, y se agregó `httpx2`, utilizado por la versión instalada de Starlette. Se comprobó mediante la jerarquía de clases que `starlette.testclient.TestClient` hereda realmente de `httpx2.Client`.

Finalmente, la aplicación se verificó con la base SQLite real y desde Swagger. Se inicializó el esquema, se levantó Uvicorn y se comprobaron las operaciones de creación, consulta, listado, actualización y eliminación. También se confirmó que los cambios se almacenaban realmente en `sensorhub.db`.

#### Decisión tomada

Se decidió conservar la arquitectura separada en routers, esquemas, dependencias, servicios, repositorios y modelos porque cada componente representa una responsabilidad diferente.

Los endpoints no realizan consultas SQLAlchemy directamente. Su función consiste en recibir los datos HTTP, delegar la operación en el servicio y transformar el resultado mediante los esquemas Pydantic.

El servicio continúa dependiendo del contrato `ReadingRepository` y no de la implementación concreta de SQLAlchemy. Esta decisión permite utilizar el repositorio real durante la ejecución y una implementación falsa durante las pruebas.

Se aceptó utilizar `Depends` para construir el servicio por petición, ya que permite controlar el ciclo de vida de la sesión y sustituir las dependencias durante las pruebas de la API.

También se decidió conservar `PATCH` para actualizaciones parciales y `DELETE` con una respuesta `204 No Content`.

El alcance se mantuvo dentro del estándar esperado. Solamente se agregó manejo HTTP básico y no se implementaron excepciones de dominio, manejadores globales ni una matriz exhaustiva de respuestas `400`, `404`, `409` y `422`.

Se decidió realizar los commits al finalizar la actividad y no crear un commit por cada fase RED, GREEN y REFACTOR, evitando fragmentar innecesariamente el historial del repositorio.

#### Cambios realizados

- Se creó `app/dependencies.py`.
- Se implementó `get_session()` para proporcionar sesiones de SQLAlchemy.
- Se implementó `get_reading_service()` para construir el repositorio y el servicio.
- Se creó `app/schemas/reading.py`.
- Se implementaron `ReadingCreate`, `ReadingUpdate` y `ReadingResponse`.
- Se amplió el contrato `ReadingRepository`.
- Se agregó paginación con `limit` y `offset`.
- Se agregaron filtros mediante `from_date` y `to_date`.
- Se implementó la consulta de lecturas por identificador.
- Se implementó la actualización de lecturas.
- Se implementó la eliminación de lecturas.
- Se amplió `ReadingService` con las operaciones CRUD.
- Se centralizaron las validaciones internas del servicio.
- Se ampliaron las pruebas unitarias de `ReadingService`.
- Se creó `app/routers/readings.py`.
- Se implementó `POST /sensors/{sensor_id}/readings`.
- Se implementó `GET /sensors/{sensor_id}/readings`.
- Se implementó `GET /readings/{reading_id}`.
- Se implementó `PATCH /readings/{reading_id}`.
- Se implementó `DELETE /readings/{reading_id}`.
- Se agregó el alias tipado `ReadingServiceDependency`.
- Se agregó el manejo básico de respuestas `400` y `404`.
- Se conservaron las validaciones automáticas `422` de FastAPI.
- Se creó `tests/test_readings_api.py`.
- Se utilizaron dependencias sustituidas mediante `dependency_overrides`.
- Se comprobaron los cinco endpoints mediante un servicio falso.
- Se reemplazó el endpoint provisional de `app/main.py`.
- `app/main.py` quedó encargado de crear la aplicación y registrar el router.
- Se conservó `GET /health`.
- Se mantuvo `httpx` por compatibilidad con la guía.
- Se agregó `httpx2` por compatibilidad con la versión instalada de Starlette.
- Se confirmó el uso de `httpx2.Client` desde `TestClient`.
- Se verificaron las pruebas automatizadas.
- Se ejecutaron Ruff y Mypy sin errores.
- Se inicializó la base SQLite real.
- Se verificaron los endpoints desde Swagger.
- Se comprobó la persistencia de las operaciones en `sensorhub.db`.
- Se documentó la decisión arquitectónica en `ADR-0003`.

#### Justificación

La inyección de dependencias permite conectar las capas sin que los endpoints necesiten conocer cómo se construyen las sesiones, los repositorios o los servicios. Esto reduce el acoplamiento y facilita sustituir los componentes durante las pruebas.

Los esquemas Pydantic mantienen separados los datos que recibe la API de los modelos utilizados por SQLAlchemy. El servicio concentra las reglas del sistema y el repositorio concentra las operaciones de persistencia.

Las pruebas HTTP con un servicio falso verifican que cada endpoint reciba correctamente los datos, invoque la operación correspondiente y genere la respuesta esperada sin depender de una base de datos durante esas comprobaciones.

La validación manual con Swagger y SQLite complementó las pruebas aisladas al demostrar que la cadena completa funciona realmente:

```text
Solicitud HTTP → Router → Servicio → Repositorio → SQLAlchemy → SQLite
```

### Viernes — Ejercicio integrador de SensorHub y cierre técnico de la API

#### Objetivo

Completar la API de SensorHub integrando la administración de sensores y lecturas dentro de una arquitectura de cuatro capas.

La actividad debía incluir:

- CRUD de sensores;
- CRUD de lecturas;
- paginación;
- filtros por rango de fechas;
- validación física según el tipo de sensor;
- persistencia con SQLAlchemy 2.x y SQLite;
- pruebas de integración con `TestClient`;
- cobertura mínima del 80 %;
- Ruff y Mypy sin errores;
- documentación funcional mediante Swagger.

También se buscó revisar críticamente las pruebas generadas durante el desarrollo para evitar casos redundantes, pruebas que dieran una falsa confianza o complejidad agregada únicamente para aumentar la cobertura.

#### Herramientas utilizadas

- ChatGPT, para analizar la guía, planificar el trabajo, explicar cada modificación y coordinar las verificaciones.
- Codex, para revisar la implementación y las pruebas en modo auditoría, sin modificar automáticamente el repositorio.
- Pytest y pytest-cov, para ejecutar las pruebas y medir la cobertura.
- Ruff y Mypy, para comprobar el estilo, la calidad y el tipado.
- Swagger, para probar manualmente la API completa.

#### Solicitud inicial realizada a la IA

> Revisa la actividad correspondiente al viernes de la Semana 3 y compara sus requisitos con el estado actual de SensorHub.
>
> Necesito completar el CRUD de sensores y lecturas, las validaciones físicas, la paginación, los filtros por fecha, la arquitectura en cuatro capas y las pruebas de integración.
>
> Guíame indicando siempre el archivo que debo crear o modificar. Mantén el desarrollo dentro del estándar esperado y no agregues características de alto potencial que no sean necesarias.
>
> No hagas commits hasta que toda la actividad esté terminada y verificada.

#### Propuesta inicial

La propuesta consistió en ampliar SensorHub con una entidad independiente para representar sensores y adaptar las lecturas para que cada registro almacenara una sola magnitud.

Se propuso crear:

- `app/sensor_types.py`;
- `app/models/sensor.py`;
- `app/repositories/sensor_repository.py`;
- `app/services/sensor_service.py`;
- `app/schemas/sensor.py`;
- `app/routers/sensors.py`.

También se propuso modificar el modelo de lecturas para utilizar:

- `sensor_id`;
- `value`;
- `unit`;
- `received_at`.

La arquitectura propuesta conservó el flujo:

```text
Router
→ Service
→ Repository
→ Model
→ SQLite
```

#### Revisión y decisiones tomadas

La propuesta no se aceptó automáticamente. Antes de continuar se revisó cómo se relacionaban los sensores con sus lecturas y qué responsabilidad correspondía a cada capa.

Se decidió conservar dos tipos de sensor:

- `temperature`, cuya unidad válida es `C`;
- `humidity`, cuya unidad válida es `%`.

Las reglas físicas definidas fueron:

- la temperatura no puede ser menor que `-273.15 °C`;
- la humedad debe estar entre `0 %` y `100 %`;
- la unidad debe coincidir con el tipo del sensor;
- no se pueden registrar lecturas para sensores inexistentes;
- no se pueden registrar lecturas para sensores desactivados.

También se decidió que eliminar un sensor significara desactivarlo mediante `is_active=False`, conservando su registro y sus lecturas históricas.

#### Cambios realizados en la implementación

Se creó el modelo ORM `Sensor` con los campos:

- `id`;
- `name`;
- `sensor_type`;
- `unit`;
- `is_active`.

Se creó un repositorio de sensores con operaciones para:

- agregar;
- listar con paginación;
- consultar por identificador;
- actualizar.

Se implementó `SensorService` con reglas para:

- normalizar identificadores y nombres;
- rechazar identificadores duplicados;
- validar la compatibilidad entre tipo y unidad;
- actualizar parcialmente un sensor;
- desactivar un sensor;
- validar `limit` y `offset`.

Se crearon los esquemas Pydantic de sensores y los endpoints:

- `POST /sensors`;
- `GET /sensors`;
- `GET /sensors/{sensor_id}`;
- `PATCH /sensors/{sensor_id}`;
- `DELETE /sensors/{sensor_id}`.

El modelo de lecturas fue adaptado para almacenar una sola medición mediante `value` y `unit`.

El servicio de lecturas se amplió para:

- consultar el sensor antes de registrar una lectura;
- comprobar que se encuentre activo;
- validar el valor y la unidad;
- listar con paginación y filtros de fecha;
- consultar una lectura por identificador;
- actualizar parcialmente una lectura;
- eliminar una lectura.

La tabla `readings` declara una clave foránea desde `sensor_id` hacia `sensors.id`.

#### Revisión de la base de datos local

La base `sensorhub.db` todavía conservaba el esquema anterior con las columnas:

- `temperature`;
- `humidity`.

Se comprobó el esquema mediante `sqlite3` y se determinó que ejecutar solamente `Base.metadata.create_all()` no modificaría una tabla existente.

Por esta razón:

1. se creó una copia de seguridad fuera del repositorio;
2. se eliminó la base local antigua;
3. se ejecutó `python -m app.init_db`;
4. se comprobó que existieran las tablas `sensors` y `readings`;
5. se confirmó la clave foránea declarada en el esquema.

La base recreada utiliza:

```text
sensors
- id
- name
- sensor_type
- unit
- is_active

readings
- id
- sensor_id
- value
- unit
- received_at
```

#### Primera auditoría de Codex

Se solicitó a Codex revisar críticamente toda la suite sin modificar archivos.

La auditoría señaló principalmente:

- pruebas de actualización que observaban el mismo objeto dentro de una sesión;
- un filtro superior de fechas que no estaba protegido correctamente;
- una prueba de persistencia redundante;
- repositorios falsos que reimplementaban demasiada lógica;
- pruebas HTTP con caminos felices duplicados;
- uso de `dependency_overrides.clear()`;
- una prueba de integración demasiado extensa;
- posible bloqueo de `TestClient`;
- ausencia de algunos contratos HTTP representativos.

Cada observación se evaluó antes de aplicar cambios.

#### Decisión sobre TestClient

Codex señaló un posible bloqueo relacionado con `TestClient`.

Antes de modificar dependencias se realizaron comprobaciones manuales:

- `GET /health` con un context manager;
- `GET /health` con cierre manual;
- una prueba HTTP aislada;
- todas las pruebas del router de lecturas;
- todas las pruebas del router de sensores;
- la prueba de integración;
- la suite completa.

Todas terminaron correctamente.

Por ello se decidió:

- no modificar `httpx`;
- no modificar `httpx2`;
- no cambiar FastAPI;
- no cambiar Starlette;
- considerar que el bloqueo no era reproducible en el entorno real.

#### Fortalecimiento de pruebas de repositorios

Las pruebas de repositorios fueron modificadas para utilizar sesiones diferentes.

El procedimiento utilizado fue:

```text
Sesión 1
→ crear o actualizar
→ commit
→ cerrar sesión

Sesión 2
→ consultar nuevamente desde SQLite
→ comprobar la persistencia real
```

En el repositorio de lecturas también se agregaron registros:

- anteriores al límite inferior;
- dentro del rango;
- posteriores al límite superior;
- pertenecientes a otro sensor.

Esto permite detectar la pérdida accidental de:

- `from_date`;
- `to_date`;
- el filtro por sensor;
- `limit`;
- `offset`.

Se eliminó `tests/test_reading_persistence.py` porque su comportamiento ya estaba cubierto de forma más útil por el repositorio real y una nueva sesión.

#### Uso de fakes como spies

Los repositorios falsos de los servicios fueron adaptados para registrar llamadas mediante atributos como:

- `add_calls`;
- `update_calls`;
- `delete_calls`;
- `get_arguments`;
- `list_arguments`.

Esto permite detectar errores como:

- modificar un objeto sin llamar al repositorio;
- no reenviar la paginación;
- no reenviar los filtros;
- no normalizar un identificador;
- no delegar una eliminación.

El fake de lecturas dejó de implementar filtros o reglas físicas, evitando que las pruebas verificaran una segunda implementación creada únicamente para el test.

#### Revisión de las pruebas HTTP

Las pruebas HTTP aisladas se redujeron para verificar contratos representativos.

En sensores se comprobaron:

- `201` al crear;
- `200` al listar;
- `400` por una regla de negocio;
- `404` por un sensor inexistente;
- `422` por un tipo inválido.

En lecturas se comprobaron:

- `201` al crear;
- `200` al listar con paginación y fechas;
- `200` al actualizar parcialmente;
- `400` por un valor físicamente inválido;
- `404` por un sensor inexistente;
- `422` por una unidad desconocida.

Se reemplazó:

```python
app.dependency_overrides.clear()
```

por la eliminación exclusiva del override utilizado en cada prueba mediante `pop()`.

También se corrigió una comparación frágil de fechas. FastAPI serializaba UTC mediante `Z`, mientras que `datetime.isoformat()` producía `+00:00`. La prueba fue modificada para convertir la respuesta nuevamente a `datetime` y comparar el valor temporal, no su representación textual.

#### División de la prueba de integración

La prueba monolítica fue dividida en dos flujos independientes.

Primer flujo:

```text
crear sensor
→ crear lectura
→ listar lecturas
→ consultar lectura por ID
```

Segundo flujo:

```text
crear y actualizar sensor
→ crear y actualizar lectura
→ eliminar lectura
→ desactivar sensor
→ rechazar una nueva lectura
```

Cada prueba utiliza:

- una base SQLite temporal diferente;
- una fixture con alcance de función;
- todas las capas reales;
- un override exclusivo de `get_session`;
- cierre del `TestClient`;
- eliminación del override;
- `engine.dispose()`.

Se decidió mantener la fixture en el archivo de integración porque no se reutiliza en otros módulos y moverla a `conftest.py` agregaría abstracción sin beneficio suficiente.

#### Segunda auditoría de Codex

Después de los cambios se solicitó una segunda auditoría completa.

Codex confirmó que:

- la arquitectura en cuatro capas era correcta;
- no existían defectos bloqueantes;
- las pruebas de repositorios verificaban persistencia real;
- eliminar la prueba redundante había sido correcto;
- los spies aportaban valor;
- el tamaño de `test_reading_service.py` estaba mayormente justificado;
- los contratos HTTP eran suficientes para el estándar esperado;
- la integración estaba correctamente dividida;
- la cobertura no estaba inflada artificialmente;
- no era necesario modificar TestClient ni sus dependencias.

La única brecha de pruebas relevante fue la actualización conjunta de `sensor_type` y `unit`.

#### Pruebas adicionales realizadas con Codex

Se solicitó a Codex modificar únicamente:

```text
tests/test_sensor_service.py
```

Se añadieron:

- una prueba para cambiar un sensor de `temperature/C` a `humidity/%`;
- dos casos parametrizados para rechazar actualizaciones incompatibles:
  - cambiar solo el tipo;
  - cambiar solo la unidad.

Se verificó que el servicio valida la combinación final antes de modificar el objeto, por lo que una actualización rechazada no deja el sensor en un estado parcial.

#### Verificaciones automatizadas finales

Al finalizar el trabajo se ejecutaron:

```bash
python -m pytest --no-cov -q
ruff check app tests
mypy app tests
git diff --check
python -m pytest
```

Resultados:

```text
58 pruebas aprobadas
Cobertura total: 88.12 %
Ruff: sin errores
Mypy: sin errores en 28 archivos
git diff --check: correcto
```

La cobertura mínima requerida era del 80 %, por lo que el resultado supera el estándar esperado.

#### Validación manual con Swagger

Se inició la aplicación mediante:

```bash
python -m uvicorn app.main:app --reload
```

Después se abrió:

```text
http://127.0.0.1:8000/docs
```

Swagger mostró correctamente:

- cinco operaciones de sensores;
- cinco operaciones de lecturas;
- `GET /health`;
- los esquemas Pydantic;
- la versión `SensorHub 0.2.0`.

Desde Swagger se comprobó el siguiente flujo:

1. consultar `GET /health`;
2. crear un sensor de temperatura;
3. consultar el sensor;
4. actualizar su nombre;
5. crear una lectura de `24.5 C`;
6. listar sus lecturas;
7. consultar la lectura por identificador;
8. actualizar el valor a `27.5 C`;
9. eliminar la lectura;
10. comprobar que la lectura devolviera `404`;
11. desactivar el sensor;
12. comprobar que permaneciera registrado con `is_active=false`;
13. intentar registrar una lectura nueva;
14. confirmar el rechazo mediante `400`.

Todas las operaciones devolvieron los códigos y datos esperados.

#### Documentación actualizada

Durante el cierre se revisaron los archivos de documentación.

Se actualizó `requirements.txt` para incluir las herramientas realmente utilizadas:

- `pytest`;
- `pytest-cov`;
- `ruff`;
- `mypy`;
- `pre-commit`.

Se reemplazó el README anterior, centrado únicamente en el driver UART, por una descripción del producto actual SensorHub.

El nuevo README documenta:

- funcionalidades;
- arquitectura;
- instalación;
- inicialización de SQLite;
- ejecución con Uvicorn;
- Swagger;
- endpoints;
- pruebas;
- historial del curso.

Se actualizó `ADR-0002` para registrar la evolución del modelo original hacia las tablas actuales de sensores y lecturas.

Se completó `ADR-0003`, que había terminado con un bloque Markdown abierto, y se documentó:

- la arquitectura en capas;
- las responsabilidades;
- la inyección de dependencias;
- el flujo de un `POST`;
- las alternativas;
- las consecuencias.

También se corrigió el bloque de código incompleto al final de la entrada del jueves en esta bitácora.

#### Decisión final

Se decidió considerar terminado el desarrollo funcional del viernes porque se cumplen:

- CRUD de sensores;
- CRUD de lecturas;
- paginación;
- filtros por fecha;
- validación física;
- arquitectura de cuatro capas;
- integración mediante `TestClient`;
- cobertura superior al 80 %;
- Ruff y Mypy sin errores;
- Swagger funcional.

No se implementaron recomendaciones opcionales como:

- validación explícita de `NaN` e infinito;
- activación de `PRAGMA foreign_keys=ON`;
- excepciones de dominio personalizadas;
- respuesta `409` para duplicados;
- cobertura artificial de `__repr__` o `init_db.py`;
- reducción de pruebas únicamente para disminuir líneas;
- traslado de fixtures a `conftest.py`.

Estas propuestas se consideraron válidas como mejoras futuras, pero no indispensables para el estándar esperado de la actividad.

#### Justificación

La inteligencia artificial se utilizó como apoyo para planificar, revisar, cuestionar y verificar el trabajo.

Las propuestas no se aceptaron automáticamente. Cada recomendación se clasificó según su impacto:

- los problemas funcionales o de falsa confianza se corrigieron;
- las mejoras pequeñas se evaluaron;
- las recomendaciones de alto potencial se descartaron cuando añadían complejidad sin aportar al objetivo de la semana.

El proceso permitió mantener una arquitectura comprensible, una suite de pruebas útil y una implementación que puede explicarse de extremo a extremo.

El flujo principal de registro de una lectura puede resumirse así:

```text
Cliente HTTP
→ Router de FastAPI
→ Schema Pydantic
→ Dependencia
→ ReadingService
→ Repositorios
→ Modelos SQLAlchemy
→ SQLite
→ ReadingResponse
→ Cliente HTTP
```

La siguiente etapa corresponde a abrir el pull request, recibir y realizar la revisión por pares, responder las observaciones y completar el cierre de la Semana 3.
## Semana 3 — Revisión por pares

### Atención de observaciones recibidas en el Pull Request

#### Objetivo

Analizar las observaciones realizadas por un compañero durante la revisión por pares del Pull Request de SensorHub y determinar cuáles requerían cambios en el código.

#### Herramienta utilizada

`ChatGPT`

#### Prompt utilizado

> Mi compañero ya comentó en mi Pull Request con observaciones y preguntas. Revisa cada comentario en relación con mi proyecto, determina si es válido y ayúdame a decidir qué cambios debo realizar antes del merge.

#### Propuesta de la IA

La IA revisó las dos observaciones técnicas y la pregunta recibida.

La primera observación indicó que `update_sensor()` permitía modificar el tipo y la unidad de un sensor aunque ya tuviera lecturas almacenadas. Esto podía dejar lecturas históricas en grados Celsius asociadas posteriormente con un sensor identificado como humedad y porcentaje.

La segunda observación señaló que el intento de registrar un sensor con un identificador existente devolvía `400 Bad Request`, aunque el código `409 Conflict` representaba mejor el conflicto con un recurso existente.

La pregunta solicitó justificar la decisión de desactivar lógicamente los sensores en lugar de eliminarlos físicamente.

#### Decisión tomada

Se decidió aceptar las dos observaciones técnicas.

El tipo y la unidad quedaron definidos únicamente durante la creación del sensor. Las actualizaciones parciales ahora permiten modificar solamente el nombre y el estado activo.

También se creó una excepción específica para representar sensores duplicados y traducir ese caso a una respuesta HTTP `409 Conflict`.

La desactivación lógica se conservó porque permite mantener el registro del sensor y sus lecturas históricas, rechazar nuevas lecturas mientras está inactivo y permitir una reactivación posterior mediante `PATCH`.

#### Cambios realizados

- Se creó `app/exceptions.py` con `SensorAlreadyExistsError`.
- Se modificó `SensorUpdate` para aceptar solamente `name` e `is_active`.
- Se configuró el esquema de actualización con `extra="forbid"`.
- Se eliminó del servicio la posibilidad de modificar `sensor_type` y `unit`.
- Se agregó una respuesta `409 Conflict` para identificadores duplicados.
- Se conservaron los demás errores de negocio como `400 Bad Request`.
- Se actualizaron las pruebas unitarias del servicio.
- Se agregaron pruebas HTTP para el código `409`.
- Se agregó una prueba que rechaza con `422` el intento de modificar el tipo y la unidad.
- Se ejecutaron nuevamente Pytest, Ruff y Mypy.

#### Resultado de la validación

```text
57 pruebas aprobadas
Cobertura total: 88.09 %
Ruff: sin errores
Mypy: sin errores en 29 archivos
```
## Semana 4

### Lunes: contenerización de SensorHub con Docker

#### Objetivo

Comprender los conceptos fundamentales de Docker y contenerizar la API SensorHub para ejecutarla en un entorno aislado y reproducible.

#### Herramientas utilizadas

- `ChatGPT`
- Tutorial oficial `Docker Get Started`
- Docker Desktop con integración WSL2

#### Prompt utilizado

> Ayúdame a revisar y comprender paso a paso el tutorial oficial de Docker. Después aplica lo aprendido a mi API SensorHub, indicando qué archivos crear, qué comandos ejecutar y cómo comprobar que la aplicación funciona dentro de un contenedor.

#### Propuesta de la IA

La IA propuso comenzar con el ejercicio oficial `getting-started-app` antes de modificar SensorHub.

Durante el ejercicio se practicó:

- la diferencia entre imagen y contenedor;
- la creación de un `Dockerfile`;
- la construcción de imágenes con `docker build`;
- la ejecución de contenedores con `docker run`;
- el mapeo de puertos;
- la actualización y reconstrucción de una imagen;
- la publicación de una imagen en Docker Hub;
- la persistencia de datos mediante volúmenes.

Después se propuso crear para SensorHub:

- un `Dockerfile` basado en `python:3.12-slim`;
- un archivo `.dockerignore`;
- un comando de inicio que crea las tablas SQLite y ejecuta Uvicorn;
- una imagen local identificada como `sensorhub:dev`;
- un contenedor llamado `sensorhub-api`.

#### Decisión tomada

Se decidió seguir primero el ejercicio oficial para comprender el ciclo completo de Docker sin alterar el proyecto principal.

Posteriormente se aplicaron los mismos conceptos a SensorHub, manteniendo SQLite para la actividad del lunes. La integración con PostgreSQL, Docker Compose y Alembic se dejó para el martes, conforme a la ruta de trabajo de la semana.

Se eligió `python:3.12-slim` porque es una imagen ligera y coincide con la versión propuesta en la guía de la Semana 4.

También se decidió copiar primero `requirements.txt` y después el código de `app/`, con el objetivo de aprovechar la caché de capas y evitar reinstalar dependencias cuando únicamente cambia el código fuente.

#### Cambios realizados

- Se creó `Dockerfile`.
- Se creó `.dockerignore`.
- Se excluyeron del contexto de construcción:
  - el entorno virtual;
  - el historial de Git;
  - las cachés de Python, Pytest, Ruff y Mypy;
  - la base de datos SQLite local;
  - las pruebas;
  - los ejercicios de semanas anteriores;
  - archivos de documentación que no son necesarios para ejecutar la API.
- Se construyó la imagen `sensorhub:dev`.
- Se creó el contenedor `sensorhub-api`.
- Se publicó el puerto interno 8000 en `127.0.0.1:8000`.
- Se inicializaron las tablas SQLite mediante `python -m app.init_db`.
- Se inició la API con Uvicorn escuchando en `0.0.0.0:8000`.

#### Resultado de la validación

Antes de contenerizar la aplicación se obtuvo:

```text
Ruff: sin errores en app y tests
Mypy: sin errores en 22 archivos
Pytest: 57 pruebas aprobadas
Cobertura total: 88.09 %
```
### Martes: Docker Compose, PostgreSQL y Alembic

#### Objetivo

Orquestar la API SensorHub y una base de datos PostgreSQL mediante Docker Compose, configurar la conexión mediante variables de entorno, comprobar la persistencia de los datos e implementar Alembic para administrar el esquema de la base de datos mediante migraciones versionadas.

#### Herramientas utilizadas

- `ChatGPT`
- Docker Desktop
- Docker Compose
- PostgreSQL 16
- SQLAlchemy 2.x
- Psycopg
- Alembic
- Pytest
- Ruff
- Mypy

#### Prompt utilizado

> Ayúdame a desarrollar paso a paso la actividad del martes de la Semana 4.
>
> Necesito levantar SensorHub y PostgreSQL mediante Docker Compose, utilizar variables de entorno sin subir secretos al repositorio, comprobar que los datos persistan mediante un volumen e inicializar Alembic con una primera migración autogenerada.
>
> Indícame los archivos que debo crear o modificar y explica el propósito de cada cambio antes de continuar.

#### Propuesta de la IA

La IA propuso separar la aplicación y la base de datos en dos servicios independientes:

```text
Docker Compose
├── api: FastAPI, SQLAlchemy y Uvicorn
└── db: PostgreSQL 16
```

También propuso:

- mantener SQLite como configuración local predeterminada;
- leer `DATABASE_URL` desde una variable de entorno;
- normalizar direcciones que comiencen con `postgres://` o `postgresql://`;
- utilizar Psycopg como controlador de PostgreSQL;
- almacenar las credenciales locales en un archivo `.env`;
- excluir `.env` mediante `.gitignore`;
- versionar solamente un archivo `.env.example`;
- declarar un health check para PostgreSQL;
- utilizar un volumen nombrado para conservar los datos;
- esperar a que PostgreSQL estuviera saludable antes de iniciar la API;
- inicializar Alembic;
- conectar Alembic con `Base.metadata`;
- generar una primera migración autogenerada;
- reemplazar la creación directa de tablas por `alembic upgrade head`;
- ejecutar las migraciones antes de iniciar Uvicorn.

#### Revisión conceptual

Antes de crear los archivos se revisó por qué la API y PostgreSQL deben encontrarse en contenedores separados.

Se comprendió que cada contenedor debe tener una responsabilidad principal:

```text
api
→ atender solicitudes HTTP;
→ validar información;
→ ejecutar reglas de negocio;
→ acceder a los repositorios.

db
→ almacenar sensores y lecturas;
→ administrar las tablas;
→ conservar los datos.
```

También se revisó que `localhost` tiene un significado diferente dentro de un contenedor.

Dentro del servicio `api`:

```text
localhost = el propio contenedor de la API
```

Por esta razón, la API no debe intentar localizar PostgreSQL mediante `localhost`. Docker Compose crea una red interna y permite localizar cada servicio mediante su nombre.

La conexión utiliza:

```text
db
```

como host de PostgreSQL:

```text
postgresql+psycopg://usuario:contraseña@db:5432/sensorhub
```

#### Decisión tomada

Se decidió utilizar dos contenedores independientes porque SensorHub y PostgreSQL tienen responsabilidades distintas.

El servicio `api` construye SensorHub mediante el `Dockerfile`, mientras que el servicio `db` utiliza la imagen oficial:

```text
postgres:16
```

Dentro de la red creada por Docker Compose, la API se conecta a PostgreSQL utilizando `db` como nombre del host.

También se decidió conservar SQLite como valor predeterminado cuando `DATABASE_URL` no esté definida. Esto permite ejecutar localmente la API y las pruebas sin depender obligatoriamente de PostgreSQL.

Las credenciales locales se almacenaron en `.env`. Este archivo está excluido por Git y no debe subirse al repositorio.

El repositorio conserva únicamente `.env.example`, que contiene valores de referencia y no una contraseña real.

Finalmente, se decidió eliminar `app/init_db.py`, porque Alembic asumió la responsabilidad de crear y versionar el esquema de la base de datos. Conservar ambos mecanismos habría duplicado responsabilidades y podría producir diferencias entre el esquema creado directamente por SQLAlchemy y el historial de migraciones.

#### Cambios realizados

##### Dependencias

Se modificó:

```text
requirements.txt
```

para agregar:

```text
psycopg[binary]
alembic
```

Psycopg permite que SQLAlchemy se comunique con PostgreSQL.

Alembic permite registrar, aplicar y revertir cambios en el esquema mediante migraciones versionadas.

##### Configuración de la base de datos

Se modificó:

```text
app/db.py
```

para obtener la conexión mediante:

```text
DATABASE_URL
```

Cuando la variable no está definida, la aplicación utiliza:

```text
sqlite:///./sensorhub.db
```

También se agregó la normalización de URLs.

Las direcciones:

```text
postgres://
postgresql://
```

se convierten a:

```text
postgresql+psycopg://
```

Además, `check_same_thread=False` se aplica únicamente cuando la conexión corresponde a SQLite, ya que es una configuración específica de ese motor.

##### Variables de entorno

Se creó:

```text
.env.example
```

con los valores de referencia:

```text
POSTGRES_USER=sensor
POSTGRES_PASSWORD=change-me
POSTGRES_DB=sensorhub
```

También se creó localmente:

```text
.env
```

con una contraseña de desarrollo.

Se comprobó que `.env` estuviera excluido por `.gitignore` mediante:

```text
git check-ignore -v .env
```

La salida confirmó que el archivo no será incluido en el historial de Git.

##### Docker Compose

Se creó:

```text
docker-compose.yml
```

con los servicios:

```text
api
db
```

El servicio `api`:

- construye la imagen desde el `Dockerfile`;
- publica el puerto 8000;
- recibe `DATABASE_URL`;
- depende de que PostgreSQL se encuentre saludable.

El servicio `db`:

- utiliza PostgreSQL 16;
- recibe usuario, contraseña y nombre de la base mediante variables;
- utiliza el volumen `pgdata`;
- ejecuta un health check mediante `pg_isready`.

Se validó la configuración mediante:

```text
docker compose config
```

sin mostrar en pantalla los valores expandidos.

##### Persistencia

Se creó el volumen nombrado:

```text
pgdata
```

Para comprobar la persistencia se realizó el siguiente procedimiento:

```text
1. Levantar API y PostgreSQL.
2. Crear un sensor mediante la API.
3. Ejecutar docker compose down.
4. Crear nuevamente los contenedores.
5. Consultar el mismo sensor.
```

El sensor continuó disponible después de eliminar y recrear los contenedores.

Esto confirmó que la información estaba almacenada en el volumen y no en la capa temporal del contenedor.

#### Configuración de Alembic

Se inicializó Alembic mediante:

```bash
alembic init migrations
```

Este comando creó:

```text
alembic.ini
migrations/
├── README
├── env.py
├── script.py.mako
└── versions/
```

Se modificó:

```text
migrations/env.py
```

para importar:

```python
from app.db import Base, get_database_url
from app.models import Reading, Sensor
```

También se configuró:

```python
target_metadata = Base.metadata
```

De esta forma, Alembic puede comparar los modelos ORM de SensorHub con el esquema existente de la base de datos.

La URL configurada en `alembic.ini` es reemplazada durante la ejecución por la dirección devuelta por:

```python
get_database_url()
```

Esto evita escribir una contraseña directamente en `alembic.ini`.

#### Primera migración autogenerada

La primera migración se generó utilizando una base SQLite temporal y vacía:

```bash
DATABASE_URL=sqlite:///./alembic_temp.db \
alembic revision --autogenerate \
  -m "esquema inicial de sensores y lecturas"
```

Se utilizó una base temporal porque el PostgreSQL inicial ya tenía sus tablas creadas mediante `app.init_db`.

Si la migración se hubiera generado comparando los modelos con esa base ya construida, Alembic habría encontrado ambos esquemas iguales y podría haber generado una migración vacía.

Alembic detectó:

- la tabla `sensors`;
- la tabla `readings`;
- la clave foránea de `readings.sensor_id`;
- el índice `ix_readings_sensor_id`.

#### Revisión de la migración

La migración autogenerada no se aceptó automáticamente.

Se revisaron las funciones:

```python
upgrade()
downgrade()
```

En `upgrade()` se confirmó que:

1. `sensors` se crea primero;
2. `readings` se crea después;
3. `readings.sensor_id` referencia a `sensors.id`;
4. se crea el índice `ix_readings_sensor_id`.

En `downgrade()` se confirmó que:

1. se elimina primero el índice;
2. se elimina después `readings`;
3. se elimina al final `sensors`.

Este orden respeta la relación entre las tablas y evita intentar eliminar una tabla mientras otra todavía depende de ella.

Ruff detectó ajustes de formato en el archivo generado automáticamente por Alembic.

Se corrigieron:

- la importación de `Sequence`;
- el orden de imports;
- el uso moderno del operador `|` para tipos;
- una línea que superaba el límite de 88 caracteres.

No se modificó la lógica de la migración.

#### Actualización del Dockerfile

Se modificó el `Dockerfile` para copiar dentro de la imagen:

```text
app/
alembic.ini
migrations/
```

El comando de inicio anterior era:

```text
python -m app.init_db
```

Se reemplazó por:

```text
python -m alembic upgrade head
```

El nuevo flujo de arranque es:

```text
alembic upgrade head
→ comprobar migraciones pendientes
→ aplicar las migraciones necesarias
→ iniciar Uvicorn
```

El comando configurado inicia la API solamente si las migraciones se aplican correctamente.

#### Prueba desde una base completamente vacía

Para comprobar que Alembic realmente podía reconstruir el esquema se ejecutó:

```text
docker compose down --volumes
```

Este comando eliminó:

- el contenedor de la API;
- el contenedor de PostgreSQL;
- la red de Compose;
- el volumen `pgdata`;
- las tablas y datos existentes.

Después se reconstruyeron los servicios:

```text
docker compose up --build -d
```

Los registros de la API mostraron:

```text
Context impl PostgresqlImpl
Running upgrade -> d615b8bbf188
```

Después de aplicar la migración, Uvicorn inició normalmente.

Dentro de PostgreSQL se comprobaron las tablas:

```text
alembic_version
readings
sensors
```

También se ejecutó:

```text
python -m alembic current
```

La revisión aplicada fue:

```text
d615b8bbf188 (head)
```

Esto confirmó que la base estaba sincronizada con la última migración disponible.

#### Eliminación de `app/init_db.py`

Se eliminó:

```text
app/init_db.py
```

porque ya no era utilizado por:

- el `Dockerfile`;
- Docker Compose;
- los endpoints;
- los servicios;
- los repositorios;
- las pruebas.

Alembic quedó como el único mecanismo vigente para administrar el esquema.

Las referencias históricas a `app.init_db` se conservaron en `AI_LOG.md` y en los ADR correspondientes, porque documentan cómo funcionaba el proyecto durante la Semana 3.

El `README.md` fue actualizado para sustituir las instrucciones vigentes de `app.init_db` por:

```text
python -m alembic upgrade head
```

#### Mejora de la cobertura

Después de eliminar `app/init_db.py`, la cobertura aumentó de:

```text
87.89 %
```

a:

```text
89.26 %
```

Se decidió elevarla por encima del 90 % mediante pruebas de comportamiento útil, evitando crear pruebas artificiales únicamente para aumentar el porcentaje.

Se creó:

```text
tests/test_infrastructure.py
```

con pruebas para:

- normalizar una URL que comienza con `postgres://`;
- normalizar una URL que comienza con `postgresql://`;
- comprobar que `get_session()` entrega una sesión de SQLAlchemy;
- comprobar que `GET /health` responde correctamente.

Estas pruebas cubren comportamiento de:

```text
app/db.py
app/dependencies.py
app/main.py
```

El resultado final fue:

```text
61 pruebas aprobadas
Cobertura total: 90.38 %
```

#### Resultado de la validación

Se ejecutaron las siguientes verificaciones:

```bash
python -m ruff check app tests migrations
mypy app
python -m pytest
docker compose config
docker compose up --build -d
docker compose logs api
curl -i http://localhost:8000/health
curl -i http://localhost:8000/sensors
```

Los resultados finales fueron:

```text
Ruff: sin errores
Mypy: sin errores
Pytest: 61 pruebas aprobadas
Cobertura total: 90.38 %
Docker Compose: configuración válida
PostgreSQL: healthy
Alembic: revisión inicial aplicada
GET /health: 200 OK
GET /sensors: 200 OK
Swagger: accesible
```

#### Justificación

Docker Compose permite declarar y reproducir el entorno completo de SensorHub mediante un solo archivo.

El flujo final es:

```text
docker compose up
→ crear la red interna
→ iniciar PostgreSQL
→ comprobar su health check
→ iniciar la API
→ Alembic revisa y aplica migraciones
→ Uvicorn inicia SensorHub
→ la API utiliza PostgreSQL mediante DATABASE_URL
```

La separación entre código y configuración permite utilizar distintos motores y credenciales sin modificar la implementación de la aplicación.

El volumen `pgdata` conserva la información aunque los contenedores sean eliminados y creados nuevamente.

Alembic permite reconstruir una base vacía y mantener un historial versionado de los cambios del esquema.

Las pruebas de infraestructura elevaron la cobertura al 90.38 % comprobando comportamiento real de configuración, sesiones y disponibilidad de la API.

#### Decisión final

Se decidió considerar terminada la actividad del martes porque se cumplen los siguientes puntos:

- Docker Compose levanta la API y PostgreSQL;
- PostgreSQL alcanza el estado `healthy`;
- la API se conecta mediante `DATABASE_URL`;
- SQLite permanece disponible como valor local predeterminado;
- las credenciales locales no se registran en Git;
- PostgreSQL conserva los datos mediante un volumen;
- Alembic administra el esquema;
- la migración inicial fue generada y revisada;
- una base vacía puede reconstruirse mediante `alembic upgrade head`;
- Ruff y Mypy terminan sin errores;
- las 61 pruebas están aprobadas;
- la cobertura alcanzó 90.38 %;
- `/health` y `/sensors` responden correctamente.

La actividad del martes queda completada con SensorHub y PostgreSQL funcionando mediante Docker Compose, persistencia por volumen, configuración protegida mediante variables de entorno y una primera migración de Alembic aplicada correctamente.

### Miércoles: integración continua con GitHub Actions

#### Objetivo

Crear un pipeline de integración continua que ejecutara automáticamente Ruff, Mypy y Pytest con cobertura al realizar un `push` o abrir un Pull Request hacia `main`.

#### Herramienta utilizada

`ChatGPT`

#### Prompt utilizado

> Ayúdame a implementar paso a paso un workflow de GitHub Actions para SensorHub. Necesito ejecutar Ruff, Mypy y Pytest con cobertura, comprender cada parte del archivo YAML, comprobar un fallo controlado y recuperar posteriormente el pipeline en verde.

#### Propuesta de la IA

La IA propuso crear:

```text
.github/workflows/ci.yml
```

con un job ejecutado en `ubuntu-latest` y Python 3.12.

El pipeline quedó organizado para:

```text
Descargar el repositorio
→ configurar Python
→ instalar dependencias
→ ejecutar Ruff
→ ejecutar Mypy
→ ejecutar Pytest y cobertura
```

También se propuso activar el workflow mediante los eventos:

```text
push
pull_request hacia main
```

Además, la IA explicó los conceptos de:

- workflow;
- evento;
- job;
- runner;
- step;
- check dentro de un Pull Request.

#### Decisión tomada

Se decidió utilizar los mismos comandos que ya habían sido validados localmente:

```bash
python -m ruff check app tests migrations
python -m mypy app
python -m pytest
```

También se decidió mantener Python 3.12 para que el entorno de GitHub Actions coincidiera con el utilizado en Docker.

Se aceptó realizar un fallo controlado modificando temporalmente una prueba para confirmar que el pipeline detectara errores reales.

#### Uso de la IA durante la validación

La IA guio el proceso para:

- crear el workflow;
- revisar su estructura;
- realizar el primer `push`;
- interpretar la ejecución exitosa;
- abrir el Pull Request;
- provocar una prueba fallida;
- localizar el error en los logs;
- restaurar la prueba correcta;
- comprobar que el pipeline regresara a verde;
- agregar el badge de CI al `README.md`.

La prueba modificada esperaba temporalmente un código `201` cuando `/health` respondía correctamente con `200`.

GitHub Actions detectó el fallo y mostró:

```text
assert 200 == 201
1 failed, 60 passed
```

Después de restaurar la prueba, los checks de `push` y `pull_request` volvieron a completarse correctamente.

#### Resultado

```text
Workflow: CI
Python: 3.12
Ruff: aprobado
Mypy: aprobado
Pytest: aprobado
Cobertura: superior al 90 %
Push: exitoso
Pull Request: exitoso
Badge de CI: agregado
```

La inteligencia artificial se utilizó como apoyo para comprender GitHub Actions, construir el archivo YAML, interpretar los resultados y diagnosticar el fallo controlado. Las modificaciones fueron revisadas y ejecutadas manualmente antes de incorporarlas al proyecto.

### Jueves: despliegue continuo en Render

#### Objetivo

Desplegar SensorHub en Render mediante un Blueprint con PostgreSQL y comprobar que la API pueda actualizarse automáticamente después de integrar cambios en `main`.

#### Herramienta utilizada

`ChatGPT`

#### Prompt utilizado

> Ayúdame a desplegar SensorHub en Render siguiendo la guía de infraestructura como código. Quiero utilizar `render.yaml`, PostgreSQL, Docker, Alembic y comprobar que la API quede disponible mediante una URL pública.

#### Uso de la IA

La IA se utilizó como guía para:

- adaptar el `Dockerfile` al puerto dinámico proporcionado por Render;
- crear y revisar `render.yaml`;
- configurar el Blueprint con `sensorhub-api` y `sensorhub-db`;
- conectar Render con el repositorio de GitHub;
- interpretar los logs del primer despliegue;
- diagnosticar un problema temporal de enrutamiento de Render;
- comprobar `/health`, `/docs` y `/openapi.json`;
- validar escritura y lectura de datos utilizando PostgreSQL de Render;
- comprobar que los datos permanecieran después de volver a desplegar la API.

#### Decisiones tomadas

Se decidió utilizar el mismo `Dockerfile` tanto localmente como en Render mediante:

```text
${PORT:-8000}
```

También se mantuvo la ejecución de:

```text
alembic upgrade head
```

antes del inicio de Uvicorn para garantizar que el esquema exista antes de recibir tráfico.

La conexión PostgreSQL se obtuvo mediante `DATABASE_URL` proporcionada automáticamente por el Blueprint, evitando almacenar credenciales en el repositorio.

#### Resultado

Se obtuvo una API pública funcional en:

```text
https://sensorhub-api-8yfj.onrender.com
```

Se comprobaron correctamente:

```text
/health       → 200 OK
/docs         → Swagger disponible
/openapi.json → 200 OK
```

También se creó el sensor `sensor-render-01`, se recuperó posteriormente mediante la API y se comprobó que continuaba almacenado después de un nuevo despliegue de la instancia.

La IA se utilizó como apoyo durante la configuración, validación e interpretación de los resultados; las decisiones y comprobaciones fueron ejecutadas manualmente.

### Viernes: cierre de la Evaluación 2

#### Herramienta utilizada

`ChatGPT`

#### Uso de la IA

La IA se utilizó como apoyo para revisar la rúbrica y el checklist final de la Semana 4, verificar los entregables construidos durante la semana y preparar las comprobaciones finales antes de la entrega.

También se utilizó para:

- revisar el funcionamiento final de Docker Compose con la API y PostgreSQL;
- comprobar el estado de Alembic y PostgreSQL;
- auditar el historial de Git en busca de posibles secretos;
- distinguir valores de ejemplo de credenciales reales;
- identificar que la URL pública de Render debía quedar documentada en el `README.md`.

#### Resultado

Se confirmó que la aplicación cumple con los requisitos del nivel **Estándar esperado**: Docker Compose con PostgreSQL, pipeline de CI funcional, despliegue público en Render, despliegue continuo demostrado y configuración mediante variables de entorno sin secretos reales detectados en el historial.

## Semana 5
#### LUNES: Actualización — Refinamiento de los ejercicios de prompting

Después de revisar la primera versión de `semana5/prompting.md`, se decidió sustituir los ejemplos iniciales de conversiones por tareas más representativas del trabajo realizado en SensorHub.

Los nuevos ejercicios se centraron en tres operaciones de una API REST:

1. Crear un endpoint `POST` para registrar una lectura.
2. Crear un endpoint `GET` para consultar lecturas con filtros y paginación.
3. Crear un endpoint `POST` para registrar un sensor.

Para cada tarea se mantuvo la comparación entre un prompt pobre y un prompt estructurado.

#### Herramienta utilizada

`GitHub Copilot Web`

Se decidió utilizar Copilot desde la versión web en lugar del chat integrado en VS Code para evitar que el prompt pobre se beneficiara automáticamente del contexto del repositorio. De esta manera, la comparación permitió observar con mayor claridad qué decisiones debía inventar la IA cuando no recibía información suficiente sobre SensorHub.

#### Resultados observados

Los prompts pobres generaron soluciones que podían ser funcionales de forma aislada, pero realizaron numerosas suposiciones sobre el proyecto. Entre ellas aparecieron frameworks, modelos, campos, bases de datos, reglas de negocio y estrategias de persistencia que no correspondían con la arquitectura actual de SensorHub.

En algunos casos Copilot llegó a mezclar en un mismo endpoint responsabilidades de API, validación y acceso directo a la base de datos.

Los prompts estructurados produjeron resultados mucho más cercanos al proyecto al especificar:

- el contexto de SensorHub;
- FastAPI y Python 3.12;
- la arquitectura en capas;
- los servicios que debían utilizarse;
- los modelos de entrada y salida;
- los códigos HTTP esperados;
- las restricciones arquitectónicas;
- el formato exacto de entrega.

Aun así, las respuestas estructuradas presentaron algunos errores, como tipos incorrectos, uso innecesario de `async` y `await`, dependencias mal inyectadas y diferencias con las firmas reales de los servicios.

#### Decisión tomada

Se conservaron los nuevos ejercicios porque permiten demostrar de forma más clara el efecto del contexto y las restricciones en tareas reales de desarrollo.

No se incorporó automáticamente ninguno de los códigos generados al proyecto. Los resultados se utilizaron únicamente como evidencia para comparar el comportamiento de la IA ante instrucciones ambiguas y estructuradas.

#### Justificación

La actualización muestra que un prompt estructurado reduce considerablemente la cantidad de decisiones que la IA debe asumir, pero no garantiza una respuesta completamente correcta.

Incluso cuando el resultado parece alineado con la arquitectura esperada, sigue siendo necesario revisar tipos, dependencias, contratos y responsabilidades antes de aceptar código generado por IA.

### — Día 2: Aider y trazabilidad con Git

#### Objetivo

Utilizar Aider para realizar un cambio asistido por inteligencia artificial directamente sobre el repositorio y comprobar cómo la herramienta mantiene trazabilidad de sus modificaciones mediante Git.

#### Herramienta utilizada

`Aider 0.86.2` conectado a OpenRouter mediante un modelo gratuito.

#### Configuración

Aider se instaló mediante:

```bash
python -m pip install aider-install
aider-install
```

Después se verificó la instalación con:

```bash
aider --version
```

La versión utilizada fue `0.86.2`.

Para utilizar un modelo se configuró OpenRouter mediante la variable de entorno `OPENROUTER_API_KEY`. El intento inicial de autenticación automática desde WSL no terminó correctamente debido al callback mediante `localhost`, por lo que se realizó la configuración manual de la clave.

#### Uso de Aider

Se inició Aider sobre el archivo:

```text
semana5/conversions.py
```

utilizando el modelo gratuito disponible mediante OpenRouter.

Se solicitó crear una función llamada `celsius_to_fahrenheit(celsius: float) -> float` que:

- convierta grados Celsius a Fahrenheit;
- utilice `type hints`;
- incluya una `docstring`;
- redondee el resultado a dos decimales;
- no agregue dependencias externas;
- no modifique otros archivos.

Aider generó la siguiente implementación:

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit y redondea a 2 decimales."""
    return round(celsius * 9 / 5 + 32, 2)
```

#### Trazabilidad en Git

Aider registró automáticamente sus cambios mediante los siguientes commits:

```text
7ac8e8b feat: add conversions module for week 5
2fbd5fc feat: add celsius_to_fahrenheit function
```

Esto permitió distinguir en el historial de Git los cambios realizados por la herramienta.

También se agregó `.aider*` al archivo `.gitignore` para evitar versionar archivos auxiliares generados por Aider.

#### Comparación con GitHub Copilot

Aider supera a Copilot Chat en la integración directa con el repositorio, ya que puede modificar archivos y registrar automáticamente los cambios mediante commits. Esto facilita revisar qué modificaciones fueron realizadas por la IA y proporciona mayor trazabilidad.

Sin embargo, Aider requiere una configuración inicial más compleja. Fue necesario instalar la herramienta, configurar un proveedor externo de modelos y utilizar una API key. Además, la autenticación automática con OpenRouter presentó problemas al trabajar desde WSL.

Copilot Chat resulta más sencillo para consultas rápidas y generación de propuestas, mientras que Aider proporciona una integración más directa con los archivos y con Git.

#### Validación

El archivo generado por Aider se verificó mediante:

```bash
ruff check semana5/conversions.py
mypy semana5/conversions.py
python -m pytest
```

`Ruff` y `Mypy` no detectaron problemas en `semana5/conversions.py`.

La ejecución completa de pruebas produjo:

```text
61 passed
Total coverage: 90.38%
```

superando el mínimo de cobertura del 80 % configurado en el proyecto.

#### Decisión

Se decidió conservar el cambio generado por Aider porque la función es sencilla, cumple con las restricciones solicitadas y pasó las comprobaciones de calidad realizadas.

La principal conclusión del ejercicio es que Aider aporta mayor trazabilidad que una conversación convencional con Copilot, pero requiere una configuración inicial más compleja y depende de un proveedor externo de modelos.

## Miércoles — Code review asistido por IA y pruebas de casos borde

### Objetivo

Utilizar IA como apoyo durante un code review real de `ReadingService`, evaluando sus sugerencias con criterio propio antes de modificar el código. La revisión se enfocó en principios SOLID, casos borde, seguridad, rendimiento y validaciones que pudieran permitir comportamientos incorrectos.

### Herramienta

Codex integrado en VS Code.

Para la primera etapa se configuró en modo de solo lectura mediante:

```toml
sandbox_mode = "read-only"
```

Esto permitió realizar la auditoría sin que la IA modificara automáticamente el repositorio.

### Primera solicitud a la IA

Se pidió a Codex revisar `app/services/reading_service.py` como un ingeniero senior durante un code review y buscar:

- posibles violaciones de SOLID;
- casos borde no manejados;
- riesgos de seguridad;
- problemas de rendimiento;
- validaciones incompletas;
- decisiones de diseño que pudieran ocasionar errores.

Se indicó explícitamente que no debía modificar archivos, generar pruebas ni reescribir completamente la clase.

### Resultado de la auditoría

Codex propuso nueve hallazgos.

Después de revisarlos individualmente se decidió no aceptar automáticamente todas sus recomendaciones.

Se consideraron relevantes:

- aceptación de valores `NaN` e infinitos en temperaturas;
- comparación de datetimes con y sin zona horaria;
- pérdida de la diferencia entre un campo PATCH omitido y un `null` explícito;
- dependencia de `ReadingService` sobre una interfaz de repositorio más amplia de la necesaria.

También se rechazaron propuestas como:

- establecer un máximo arbitrario para `offset`;
- agregar validaciones de tipos duplicadas en el servicio;
- cambiar el orden de algunas consultas solamente por rendimiento;
- introducir una unidad de trabajo o cambios transaccionales sin evidencia suficiente;
- agregar nuevas reglas de negocio que SensorHub no define.

### Segunda solicitud a la IA

Se pidió a Codex revisar las pruebas existentes e identificar únicamente casos borde todavía no cubiertos.

La IA analizó especialmente:

- valores nulos;
- límites exactos;
- `NaN` e infinito;
- IDs inválidos;
- fechas malformadas;
- datetimes con distinta conciencia de zona horaria;
- diferencias entre campos PATCH omitidos y enviados como `null`.

A partir de sus propuestas se seleccionaron ocho pruebas nuevas con valor para el proyecto.

### Pruebas seleccionadas

Se agregaron casos para comprobar:

1. rechazo de temperatura `NaN`;
2. rechazo de temperatura `+Infinity`;
3. rechazo controlado de un rango con datetime naive y timezone-aware;
4. rechazo de `value: null` explícito en PATCH;
5. rechazo de `unit: null` explícito en PATCH;
6. aceptación de temperatura exactamente `-273.15 °C`;
7. aceptación de humedad exactamente `0 %`;
8. aceptación de humedad exactamente `100 %`.

La IA recibió la instrucción de modificar únicamente los archivos de pruebas y no corregir todavía el código de producción.

### Evidencia RED

Se ejecutó:

```bash
python -m pytest tests/test_reading_service.py tests/test_readings_api.py -q
```

Resultado:

```text
5 failed, 31 passed
```

Los cinco fallos confirmaron defectos reales:

- `NaN` era aceptado como temperatura;
- `+Infinity` era aceptado como temperatura;
- mezclar datetime naive y timezone-aware provocaba `TypeError`;
- PATCH con `value: null` respondía `200`;
- PATCH con `unit: null` respondía `200`.

Los tres límites físicos exactos ya funcionaban correctamente.

### Correcciones solicitadas a Codex

Después de comprobar los fallos se permitió a Codex modificar únicamente:

- `app/services/reading_service.py`;
- `app/schemas/reading.py`.

Se pidió realizar únicamente las correcciones mínimas necesarias y no modificar las pruebas.

Codex implementó:

- `math.isfinite()` para rechazar mediciones no finitas;
- validación previa para impedir comparaciones entre datetimes naive y timezone-aware;
- un `field_validator` de Pydantic para rechazar `null` explícito en los campos opcionales de `ReadingUpdate`, manteniendo válidos los campos omitidos.

Los cambios fueron revisados manualmente mediante `git diff` antes de aceptar el resultado.

### Evidencia GREEN

Después de revisar las modificaciones se ejecutó:

```bash
python -m pytest tests/test_reading_service.py tests/test_readings_api.py -q --no-cov
```

Resultado:

```text
36 passed
```

Los cinco fallos detectados previamente quedaron corregidos.

### Refactor ISP

También se aceptó un hallazgo relacionado con Interface Segregation Principle.

`ReadingService` utilizaba únicamente `get_by_id()` del repositorio de sensores, pero dependía del contrato completo `SensorRepository`.

Se pidió a Codex realizar un refactor mínimo.

Se agregó:

```python
class SensorLookupRepository(Protocol):
    def get_by_id(self, sensor_id: str) -> Sensor | None:
        ...
```

`ReadingService` pasó a depender de este protocolo reducido.

`SensorRepository` y `SQLAlchemySensorRepository` conservaron su comportamiento y la implementación concreta continuó siendo compatible mediante structural typing.

### Validación final

Se ejecutaron los controles del proyecto:

```bash
python -m ruff check app tests migrations
```

Resultado: sin errores.

```bash
python -m mypy app
```

Resultado: sin errores.

Finalmente:

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

El proyecto continúa por encima del mínimo requerido de 80 %.

### Decisión

Se conservaron únicamente los cambios respaldados por pruebas reproducibles o por una mejora de diseño claramente justificable.

La IA se utilizó como herramienta de auditoría, generación de casos borde y apoyo para implementar correcciones mínimas, pero cada propuesta fue revisada antes de incorporarse.

El flujo utilizado fue:

```text
Auditoría con IA
→ evaluación humana
→ selección de casos borde
→ pruebas RED
→ corrección mínima
→ pruebas GREEN
→ validación final
```

Esta actividad mostró que un code review asistido por IA resulta útil cuando sus sugerencias se tratan como propuestas que deben comprobarse y no como cambios que deban aceptarse automáticamente.