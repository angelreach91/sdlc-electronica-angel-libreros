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

