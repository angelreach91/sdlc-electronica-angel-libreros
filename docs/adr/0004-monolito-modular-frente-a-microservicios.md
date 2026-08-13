# ADR-0004: Monolito modular frente a microservicios

- Estado: Aceptado
- Fecha: 2026-08-13

## Contexto

SensorHub se despliega actualmente como una sola aplicación FastAPI. Este modelo de despliegue no implica que el código carezca de estructura interna: la aplicación separa las responsabilidades en `routers`, `services`, `repositories`, `schemas` y `models`, de acuerdo con ADR-0003.

Los routers atienden las solicitudes HTTP y delegan las operaciones en servicios. Los servicios contienen las reglas de negocio y dependen de contratos de repositorio definidos mediante `Protocol`, no de implementaciones concretas de SQLAlchemy. Los repositorios concentran la persistencia, mientras que los esquemas Pydantic y los modelos ORM representan contratos diferentes. `app/dependencies.py` construye y conecta estas dependencias.

Esta separación permite probar las capas de manera independiente y conserva límites internos entre presentación, negocio y persistencia. Sensores y lecturas también tienen componentes separados dentro de esas capas, aunque forman parte del mismo proceso y del mismo despliegue.

Una arquitectura de microservicios puede permitir el despliegue y el escalado independientes de sus componentes. A cambio, convierte algunas llamadas locales en comunicación remota e introduce costos adicionales: operación de varios servicios, automatización de despliegues y observabilidad, compatibilidad entre contratos, tolerancia a fallos distribuidos y manejo de consistencia entre servicios.

Martin Fowler denomina *microservice premium* a este costo adicional, que debe compensarse con beneficios concretos. Su enfoque *Monolith First* propone descubrir y estabilizar primero los límites del dominio antes de convertirlos en fronteras de red. Esto no significa construir un sistema desorganizado: un monolito con límites internos claros puede facilitar una separación posterior si llega a ser necesaria.

SensorHub no tiene actualmente una necesidad demostrada de desplegar o escalar sensores y lecturas de forma independiente. Aplicando YAGNI, no se introducirá complejidad distribuida para necesidades que el sistema todavía no ha demostrado.

## Decisión

SensorHub se mantendrá por ahora como un monolito modular: una sola aplicación y una sola unidad de despliegue, con responsabilidades separadas internamente.

Se conservarán los límites y mecanismos actuales:

- routers para la interfaz HTTP;
- servicios para las reglas de negocio;
- repositorios para el acceso a datos;
- esquemas Pydantic separados de los modelos ORM;
- inyección de dependencias para construir los componentes;
- contratos `Protocol` para desacoplar los servicios de las implementaciones concretas de persistencia;
- pruebas independientes por capa.

Esta decisión no propone implementar microservicios ni define una partición futura. La eventual separación deberá basarse en evidencia y en límites de dominio maduros, no solamente en la estructura actual de carpetas.

## Alternativas consideradas

### Dividir ahora SensorHub en microservicios

Esta alternativa permitiría establecer unidades de despliegue independientes, por ejemplo para capacidades relacionadas con sensores y lecturas. Sin embargo, no existe actualmente una necesidad demostrada de desplegarlas o escalarlas por separado.

Adoptarla ahora requeriría definir fronteras de red y asumir comunicación remota, automatización operativa, observabilidad entre servicios, manejo de fallos parciales y decisiones de consistencia. El costo del *microservice premium* no está justificado por beneficios comprobados en la situación actual de SensorHub.

No se descarta como arquitectura futura; se pospone hasta que existan razones concretas que compensen su complejidad.

### Mantener un monolito sin límites internos explícitos

Esta alternativa conservaría una única unidad de despliegue, pero permitiría mezclar responsabilidades y acoplar presentación, negocio y persistencia.

Se descarta porque debilitaría la capacidad de probar las capas de forma independiente, dificultaría comprender las dependencias y haría más costosa una posible separación futura. Mantener un monolito no elimina la necesidad de modularidad.

## Consecuencias

### Positivas

- Se conserva un despliegue único y un modelo operativo sencillo.
- Las llamadas entre componentes permanecen locales y no requieren contratos de red.
- Las operaciones entre sensores y lecturas permanecen dentro de la misma aplicación y no requieren coordinación distribuida entre servicios.
- Se aprovecha la separación existente entre routers, servicios, repositorios, esquemas y modelos.
- La inyección de dependencias y los contratos `Protocol` mantienen desacopladas las reglas de negocio de la persistencia concreta.
- Las capas pueden seguir probándose de forma independiente.
- El equipo puede aprender y refinar los límites del dominio antes de convertirlos en límites de despliegue.
- Se evita asumir el *microservice premium* sin una necesidad demostrada, de acuerdo con YAGNI.

### Negativas

- Todos los componentes continúan formando parte de la misma unidad de despliegue.
- No es posible desplegar o escalar de manera independiente sensores y lecturas mientras permanezcan dentro del monolito.
- Un fallo que afecte al proceso de la aplicación puede afectar a todas sus capacidades.
- Los límites internos dependen de convenciones, contratos y disciplina arquitectónica; no están impuestos por fronteras de red.
- Si en el futuro se justifican microservicios, será necesario diseñar la separación, los contratos remotos y la estrategia de datos correspondiente.

Estas consecuencias describen compromisos del modelo elegido, no problemas de escalabilidad observados actualmente en SensorHub.

## Condiciones que podrían justificar revisar esta decisión

La decisión deberá reconsiderarse si aparece evidencia de una o más de las siguientes condiciones:

- necesidad real de escalar componentes de forma independiente;
- necesidad de desplegar componentes de forma independiente;
- límites de dominio maduros y estables que puedan convertirse en fronteras de servicio;
- equipos diferentes responsables de capacidades distintas;
- necesidades tecnológicas claramente diferentes entre componentes.

La presencia de alguna condición iniciaría una nueva evaluación arquitectónica. No implicaría automáticamente adoptar microservicios: sus beneficios, costos y alternativas deberán analizarse con la evidencia disponible en ese momento.

## Resultado

Se mantiene SensorHub como un monolito modular en su etapa actual. La aplicación seguirá desplegándose como una sola unidad y conservará su separación interna, inyección de dependencias, contratos mediante `Protocol` y capacidad de probar las capas por separado.

Los microservicios permanecen como una opción válida para una situación futura que demuestre necesidades concretas de independencia.

## Referencias

- Martin Fowler y James Lewis, [Microservices](https://martinfowler.com/articles/microservices.html).
- Martin Fowler, [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html).
