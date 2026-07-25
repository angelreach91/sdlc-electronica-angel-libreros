# Sprint Retrospective — Evaluación 1

## Qué salió bien

Durante el Sprint se logró completar el flujo principal de procesamiento de lecturas de sensores, desde la recepción y validación de los datos hasta la detección de anomalías y la generación de alertas.

El desarrollo se realizó aplicando TDD mediante commits separados para las fases RED, GREEN y REFACTOR. Esto permitió definir primero el comportamiento esperado, implementar únicamente lo necesario para satisfacer las pruebas y después mejorar la estructura interna sin modificar el funcionamiento comprobado.

También se aplicaron principios SOLID al separar la publicación de alertas mediante una estrategia abstracta, una estrategia de consola, una estrategia de archivo y un administrador encargado de coordinarlas. La inyección de estas estrategias permite agregar nuevas salidas sin modificar el comportamiento central.

La validación final confirmó que las 44 pruebas de la Semana 2 se ejecutan correctamente mediante el comando estándar y que el proyecto alcanza el 100 % de cobertura, superando el mínimo requerido del 80 %. Ruff y Mypy también finalizaron sin errores.

## Qué debe mejorar

La revisión final mostró que algunas afirmaciones de la documentación no coincidían completamente con el código presente en `main`. En particular, se había documentado un refactor de `AlertPublisher` que todavía no estaba implementado en la versión fusionada.

También se detectó que la configuración de Pytest solamente recopilaba las pruebas ubicadas en `semana2/tests`, dejando fuera las correspondientes a `semana2/eval1/tests`. Aunque las pruebas funcionaban al indicar manualmente la ruta, el comando estándar no validaba toda la Semana 2.

Estas situaciones muestran que no es suficiente comprobar cada cambio de manera aislada. Antes de cerrar un Sprint también es necesario validar el estado final de la rama principal y comparar las afirmaciones de la documentación con la implementación realmente fusionada.

## Acción concreta y verificable

Antes de cerrar el siguiente Sprint se ejecutará, desde la raíz del repositorio y sobre la rama actualizada con `main`, la siguiente validación:

```bash
python -m pytest -q
ruff check semana2
mypy semana2
git status