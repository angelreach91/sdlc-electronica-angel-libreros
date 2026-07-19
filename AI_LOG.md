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