# Apuntes de la Guía Scrum 2020

Scrum es un marco de trabajo utilizado para desarrollar soluciones a problemas
complejos. El trabajo se organiza en periodos cortos llamados Sprints, durante
los cuales el equipo construye un incremento funcional, inspecciona los
resultados y adapta el trabajo siguiente.

## 1. Roles o responsabilidades de Scrum

Aunque comúnmente se les llama roles, la Guía Scrum 2020 los define como
responsabilidades dentro del Scrum Team.

| Responsabilidad | Función principal |
|---|---|
| Product Owner | Maximiza el valor del producto, comunica el Product Goal y ordena los elementos del Product Backlog según su importancia. |
| Scrum Master | Ayuda al equipo y a la organización a comprender y aplicar Scrum correctamente. También promueve la eliminación de impedimentos y procura que los eventos sean productivos. |
| Developers | Crean el Increment durante cada Sprint, elaboran el Sprint Backlog, mantienen la calidad y adaptan diariamente su plan para alcanzar el Sprint Goal. |

El Scrum Team está formado por un Product Owner, un Scrum Master y los
Developers. Es un equipo autogestionado, por lo que sus integrantes deciden
internamente quién realiza el trabajo, cuándo y cómo.

## 2. Eventos de Scrum y sus timeboxes

Un timebox es el tiempo máximo establecido para realizar un evento. Los tiempos
indicados por la guía toman como referencia un Sprint de un mes.

| Evento | Propósito | Timebox |
|---|---|---|
| Sprint | Periodo durante el cual se transforma una selección de trabajo en un Increment de valor. Contiene todos los demás eventos. | Un mes o menos. |
| Sprint Planning | Define por qué el Sprint es valioso, qué trabajo puede completarse y cómo se realizará. | Máximo 8 horas para un Sprint de un mes. |
| Daily Scrum | Inspecciona el avance hacia el Sprint Goal y permite adaptar el plan de trabajo. | 15 minutos cada día laborable. |
| Sprint Review | Inspecciona el resultado del Sprint con los interesados y determina posibles adaptaciones del producto. | Máximo 4 horas para un Sprint de un mes. |
| Sprint Retrospective | Analiza la forma de trabajar y establece mejoras para aumentar la calidad y efectividad del equipo. | Máximo 3 horas para un Sprint de un mes. |

En Sprints con una duración menor a un mes, la Sprint Planning, Sprint Review y
Sprint Retrospective normalmente tienen una duración menor.

## 3. Artefactos y compromisos

Los artefactos hacen visible el trabajo y el valor generado. Cada artefacto
tiene un compromiso que permite medir el avance.

| Artefacto | Descripción | Compromiso |
|---|---|---|
| Product Backlog | Lista ordenada y cambiante de todo lo necesario para mejorar el producto. | Product Goal |
| Sprint Backlog | Contiene el Sprint Goal, los elementos seleccionados del Product Backlog y el plan para entregar el Increment. | Sprint Goal |
| Increment | Resultado funcional, verificado y utilizable que acerca el producto a su objetivo. | Definition of Done |

### Product Goal

Es el objetivo de largo plazo del producto. Sirve como referencia para ordenar
y planificar el trabajo contenido en el Product Backlog.

### Sprint Goal

Es el objetivo específico que el equipo busca alcanzar durante el Sprint.
Proporciona dirección y permite que los Developers mantengan un enfoque común.

### Definition of Done

Es la descripción formal de las condiciones de calidad que debe cumplir el
Increment para considerarse terminado y utilizable.

## 4. Valores de Scrum

| Valor | Significado |
|---|---|
| Compromiso | El equipo se compromete con sus objetivos y con apoyar a sus integrantes. |
| Enfoque | La atención se concentra en el trabajo necesario para alcanzar el Sprint Goal. |
| Apertura | El equipo comunica con honestidad el estado del trabajo, los problemas y los desafíos. |
| Respeto | Los integrantes reconocen las capacidades, responsabilidades e ideas de los demás. |
| Valentía | El equipo enfrenta problemas difíciles y toma decisiones correctas, aunque resulten complicadas. |

Estos valores orientan las decisiones y el comportamiento del Scrum Team y
favorecen la transparencia, la inspección y la adaptación.

## 5. Diferencia entre Definition of Done y criterios de aceptación

La Definition of Done y los criterios de aceptación se utilizan para comprobar
el trabajo, pero tienen alcances diferentes.

| Aspecto | Definition of Done | Criterios de aceptación |
|---|---|---|
| Alcance | Se aplica de manera general al Increment y al producto. | Se aplican a un elemento o funcionalidad específica. |
| Propósito | Establece el nivel de calidad necesario para considerar terminado el trabajo. | Define el comportamiento o resultado que debe cumplir una necesidad particular. |
| Pregunta que responde | ¿El trabajo tiene la calidad necesaria para considerarse terminado y utilizable? | ¿La funcionalidad hace exactamente lo que se solicitó? |
| Aplicación | Debe cumplirse en todos los elementos terminados. | Cambia dependiendo de cada elemento del Product Backlog. |
| Relación con Scrum | Es el compromiso formal asociado con el Increment. | Es una práctica complementaria; no es un elemento formal definido por la Guía Scrum. |

### Ejemplo aplicado al repositorio

Para una funcionalidad que registra mensajes UART en formato JSON, sus criterios
de aceptación podrían ser:

- Cada registro generado debe ser un objeto JSON válido.
- El registro debe contener fecha y hora, nivel, logger y evento.
- Los caracteres Unicode deben conservarse correctamente.
- Los datos no serializables deben producir un error controlado.

Una posible Definition of Done general para el proyecto sería:

- La funcionalidad cumple sus criterios de aceptación.
- El código está implementado y puede ejecutarse.
- Todas las pruebas automatizadas pasan correctamente.
- Los cambios no afectan negativamente las funciones anteriores.
- El código es comprensible y mantiene la estructura del proyecto.
- La documentación relacionada está actualizada.
- Los cambios están registrados correctamente en el repositorio.

Por lo tanto, una funcionalidad puede cumplir sus criterios de aceptación y aun
así no estar terminada si no cumple la Definition of Done. Por ejemplo, podría
producir el resultado solicitado, pero todavía carecer de pruebas o
documentación.

## Fuente consultada

- Schwaber, K. y Sutherland, J. (2020). [The Scrum Guide](https://scrumguides.org/scrum-guide.html).