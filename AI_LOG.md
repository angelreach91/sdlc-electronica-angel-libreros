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

También se omitió la prueba de serialización porque todavía no comprendía con suficiente claridad la necesidad de verificar el formato exacto en `bytes`.

Se decidió conservar cuatro pruebas sencillas y distintas entre sí. Estas permiten comprobar un cálculo correcto, una condición de error, una comparación booleana y una clasificación.

La selección final prioriza que cada línea pueda ser entendida y explicada, en lugar de mantener una batería más extensa solo por haber sido generada por la IA.