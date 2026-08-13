# Prompting efectivo — Semana 5

## Objetivo

Comparar los resultados obtenidos mediante prompts poco específicos y prompts estructurados al solicitar tareas de programación relacionadas con **SensorHub**.

Para los prompts estructurados se utilizará la siguiente organización:

- **Contexto:** qué sistema se está desarrollando y qué tecnologías utiliza.
- **Tarea:** qué se solicita realizar exactamente.
- **Restricciones:** condiciones que debe respetar la solución.
- **Entrega:** formato esperado de la respuesta.

---

## Tarea 1 — Conversión de Celsius a Fahrenheit

### Prompt pobre

> Haz una función para convertir Celsius a Fahrenheit.

### Resultado del prompt pobre

```python
celsius = 25
fahrenheit = (celsius * 9 / 5) + 32
print(f"{celsius}°C = {fahrenheit}°F")
```

### Prompt estructurado

> **CONTEXTO:** API SensorHub desarrollada con Python 3.12 y FastAPI para gestionar lecturas de sensores. El proyecto utiliza `type hints` y busca mantener funciones pequeñas y fáciles de probar.
>
> **TAREA:** Escribe una función pura llamada `celsius_to_fahrenheit(celsius: float) -> float` que convierta una temperatura de grados Celsius a grados Fahrenheit.
>
> **RESTRICCIONES:** Utiliza `type hints` completos, incluye una `docstring`, no uses dependencias externas y redondea el resultado a 2 decimales.
>
> **ENTREGA:** Devuelve únicamente la función solicitada, sin explicaciones adicionales.

### Resultado del prompt estructurado

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convierte una temperatura de grados Celsius a grados Fahrenheit.

    Args:
        celsius: Temperatura en grados Celsius.

    Returns:
        Temperatura convertida en grados Fahrenheit, redondeada a 2 decimales.
    """
    fahrenheit = (celsius * 9 / 5) + 32
    return round(fahrenheit, 2)
```

### Comparación

Los dos resultados realizan correctamente la conversión de Celsius a Fahrenheit, pero presentan diferencias importantes en su estructura.

Con el prompt pobre, Copilot generó un ejemplo específico utilizando el valor de `25 °C` y mostrando el resultado mediante `print()`. Aunque el prompt solicitaba una función, la respuesta no creó una función reutilizable ni definió tipos, documentación o precisión del resultado.

En cambio, el prompt estructurado produjo exactamente la función solicitada, con el nombre `celsius_to_fahrenheit`, `type hints`, una `docstring` y redondeo a dos decimales. Además, al recibir la temperatura como parámetro y devolver el resultado mediante `return`, la función puede reutilizarse y probarse fácilmente dentro del proyecto.

Esto muestra que proporcionar contexto, una tarea específica, restricciones y un formato de entrega reduce la ambigüedad y permite obtener un resultado más alineado con los requisitos del proyecto.

---

## Tarea 2 — Conversión de Fahrenheit a Celsius

### Prompt pobre

> Haz una función para convertir Fahrenheit a Celsius.

### Resultado del prompt pobre

```python
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9
```

### Prompt estructurado

> **CONTEXTO:** API SensorHub desarrollada con Python 3.12 y FastAPI para gestionar lecturas de sensores. El proyecto utiliza `type hints` y funciones pequeñas que puedan probarse de manera independiente.
>
> **TAREA:** Escribe una función pura llamada `fahrenheit_to_celsius(fahrenheit: float) -> float` que convierta una temperatura de grados Fahrenheit a grados Celsius.
>
> **RESTRICCIONES:** Utiliza `type hints` completos, incluye una `docstring`, no uses dependencias externas y redondea el resultado a 2 decimales.
>
> **ENTREGA:** Devuelve únicamente la función solicitada, sin explicaciones adicionales.

### Resultado del prompt estructurado

```python
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convierte una temperatura de grados Fahrenheit a grados Celsius.

    Args:
        fahrenheit: Temperatura en grados Fahrenheit.

    Returns:
        Temperatura en grados Celsius redondeada a 2 decimales.
    """
    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 2)
```

### Comparación

Ambos prompts generaron una función correcta para convertir grados Fahrenheit a Celsius.

Sin embargo, el prompt pobre produjo una solución básica que únicamente realiza la operación matemática y utiliza `type hints`, dejando sin definir aspectos como la documentación y la precisión del resultado.

En cambio, el prompt estructurado hizo que Copilot cumpliera requisitos específicos: agregó una `docstring` detallada, mantuvo los `type hints` y redondeó el resultado a dos decimales.

Esto demuestra que proporcionar contexto, restricciones y un formato de entrega permite obtener una solución más alineada con las necesidades del proyecto y reduce las decisiones que quedan a criterio de la IA.

---

## Tarea 3 — Conversión de humedad porcentual a fracción

### Prompt pobre

> Haz una función para convertir humedad a decimal.

### Resultado del prompt pobre

```python
def humidity_percentage_to_ratio(humidity: float) -> float:
    """Convierte un porcentaje de humedad a una fracción decimal entre 0.0 y 1.0."""
    if not 0.0 <= humidity <= 100.0:
        raise ValueError("La humedad debe estar entre 0 y 100.")
    return humidity / 100
```

### Prompt estructurado

> **CONTEXTO:** API SensorHub desarrollada con Python 3.12 y FastAPI para almacenar y procesar lecturas de sensores. La humedad relativa del sistema se representa normalmente como un porcentaje entre 0 y 100.
>
> **TAREA:** Escribe una función pura llamada `humidity_percentage_to_ratio(humidity: float) -> float` que convierta un porcentaje de humedad relativa a una fracción entre `0.0` y `1.0`.
>
> **RESTRICCIONES:** Utiliza `type hints` completos, incluye una `docstring`, no uses dependencias externas, valida que la entrada se encuentre entre 0 y 100 y genera `ValueError` cuando esté fuera de ese intervalo.
>
> **ENTREGA:** Devuelve únicamente la función solicitada, sin explicaciones adicionales.

### Resultado del prompt estructurado

```python
def humidity_percentage_to_ratio(humidity: float) -> float:
    """
    Convert relative humidity percentage to a ratio between 0.0 and 1.0.

    Args:
        humidity: Relative humidity as a percentage (0-100).

    Returns:
        Relative humidity as a ratio (0.0-1.0).

    Raises:
        ValueError: If humidity is not between 0 and 100.
    """
    if not (0 <= humidity <= 100):
        raise ValueError(f"Humidity must be between 0 and 100, got {humidity}")
    return humidity / 100.0
```

### Comparación

Ambos prompts produjeron una función correcta que convierte el porcentaje de humedad a una fracción entre `0.0` y `1.0`.

Incluso con el prompt pobre, Copilot agregó `type hints`, una `docstring`, validación del rango permitido y una excepción `ValueError` para valores fuera de 0 a 100.

El prompt estructurado produjo una solución muy similar, pero con una documentación más detallada y un mensaje de error más informativo que incluye el valor recibido.

Aunque en este caso la diferencia en el código fue pequeña, el prompt estructurado permitió especificar de manera explícita el comportamiento esperado y redujo la posibilidad de que la IA interpretara de otra forma qué significaba convertir la humedad a decimal.

---

## Conclusión

Las tres comparaciones muestran que un prompt poco específico puede producir resultados correctos, pero deja varias decisiones a criterio de la IA.

En la **Tarea 1**, la falta de precisión provocó que Copilot generara un ejemplo específico en lugar de una función reutilizable.

En la **Tarea 2**, el prompt estructurado permitió obtener una solución mejor documentada y con control sobre la precisión del resultado.

En la **Tarea 3**, incluso el prompt pobre produjo una solución bastante completa, aunque el prompt estructurado permitió definir explícitamente el comportamiento esperado.

Los prompts estructurados permiten definir con mayor precisión el **contexto**, la **tarea**, las **restricciones** y el **formato de entrega**. Esto no garantiza que el código generado sea siempre mejor, pero hace que el resultado sea más predecible y esté más alineado con las necesidades del proyecto.

Por lo tanto, la principal ventaja de un buen prompt no es necesariamente obtener más código, sino **reducir la ambigüedad y tener mayor control sobre lo que genera la IA**.
