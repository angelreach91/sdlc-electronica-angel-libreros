# Definition of Done

Una historia de usuario se considera terminada únicamente cuando cumple todos los criterios establecidos en esta Definition of Done.

## Criterios funcionales

- [ ] Todos los criterios de aceptación de la historia están implementados.
- [ ] Los escenarios Gherkin están representados mediante pruebas automatizadas.
- [ ] Se comprobaron los casos normales, casos de error y casos borde.
- [ ] La funcionalidad presenta el comportamiento esperado.

## Desarrollo mediante TDD

- [ ] Se siguió el ciclo RED → GREEN → REFACTOR.
- [ ] Se creó primero una prueba que fallara por la ausencia del comportamiento.
- [ ] Se implementó el código mínimo necesario para aprobar la prueba.
- [ ] Se refactorizó el código sin alterar su comportamiento.
- [ ] Los commits permiten identificar la evolución del ciclo TDD.

## Calidad automatizada

- [ ] Todas las pruebas automatizadas pasan correctamente.
- [ ] La cobertura de pruebas es igual o superior al 80 %.
- [ ] Ruff no reporta errores con las reglas `E`, `F`, `I`, `UP` y `B`.
- [ ] Mypy no reporta errores de tipado.
- [ ] Todas las funciones cuentan con anotaciones de tipo.

## Revisión y documentación

- [ ] El código es legible y mantiene responsabilidades claras.
- [ ] La documentación relacionada con la funcionalidad está actualizada.
- [ ] El uso de inteligencia artificial está documentado en `AI_LOG.md`.
- [ ] Los cambios fueron revisados en la pestaña `Files changed` del Pull Request.
- [ ] La auto-revisión quedó documentada antes de realizar el merge.

## Control de versiones

- [ ] El trabajo se realizó en una rama independiente.
- [ ] Los commits son claros y representan cambios concretos.
- [ ] La rama fue publicada en GitHub.
- [ ] Se abrió un Pull Request hacia `main`.
- [ ] Todas las comprobaciones se ejecutaron antes del merge.
- [ ] Los cambios fueron fusionados en `main`.


## Evidencia de cumplimiento — Sprint 1

| Criterio | Evidencia | Estado |
|---|---|---|
| Los criterios de aceptación están representados mediante pruebas | Pruebas automatizadas en `semana2/tests` y `semana2/eval1/tests` | Cumplido |
| Existe evidencia de RED, GREEN y REFACTOR | Commits separados y Pull Requests del desarrollo de las historias | Cumplido |
| Todas las pruebas están aprobadas | `python -m pytest -q`: 44 pruebas aprobadas | Cumplido |
| La cobertura es igual o superior al 80 % | Cobertura final: 100 % | Cumplido |
| Ruff finaliza sin errores | `ruff check semana2` | Cumplido |
| Mypy finaliza sin errores | `mypy semana2` | Cumplido |
| El código mantiene responsabilidades separadas | Uso de `AlertStrategy`, `ConsoleAlertStrategy`, `FileAlertStrategy` y `AlertManager` | Cumplido |
| Las decisiones relacionadas con IA están documentadas | Entradas correspondientes en `AI_LOG.md` | Cumplido |
| Los cambios fueron revisados antes de fusionarse | Pull Requests utilizados durante el Sprint | Cumplido |
| El incremento se encuentra integrado en `main` | Validación final realizada sobre la rama actualizada | Cumplido |

## Resultado

El Sprint 1 cumple con la Definition of Done establecida. Las siete historias seleccionadas pueden considerarse terminadas.