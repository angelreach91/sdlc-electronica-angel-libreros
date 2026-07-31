# ADR-0003: Arquitectura en capas e inyección de dependencias para SensorHub

- Estado: Aceptado
- Fecha: 2026-07-30

## Contexto

SensorHub ya contaba con una aplicación inicial de FastAPI, un modelo ORM, persistencia con SQLite, un repositorio y un servicio de lecturas.

Sin embargo, la primera versión de la API todavía concentraba los esquemas y los endpoints en `app/main.py`. Además, el endpoint inicial solamente construía una respuesta en memoria y no utilizaba la persistencia desarrollada con SQLAlchemy.

Era necesario conectar FastAPI con las capas internas del sistema sin colocar consultas, sesiones ni reglas de negocio directamente dentro de los endpoints.

La API también debía ofrecer operaciones para crear, consultar, actualizar y eliminar lecturas, además de permitir paginación y filtros por fecha.

## Decisión

Se utilizará una arquitectura organizada en las siguientes capas:

```text
Router → Servicio → Repositorio → SQLAlchemy → SQLite