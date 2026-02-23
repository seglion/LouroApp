# ADR-001: Uso de UUIDv7 generados en el frontend para prevención de conflictos clave

## Status
Accepted

## Context
El sistema de recolección en campo (PWA) operará frecuentemente offline. Los técnicos crearán registros complejos (pozo -> acometidas -> imágenes) que requieren mantener integridad referencial a nivel local antes de llegar al servidor. El uso de IDs secuenciales dependientes de la base de datos central generaría dependencias bloqueantes y alta probabilidad de colisión al consolidar los datos de múltiples tablets.

## Decision
Utilizar **UUIDv7** generado directamente en el cliente (PWA Vue.js) al momento de la captura, usándolo como clave primaria (PK) definitiva en todo el stack.

## Rationale
*   **Descentralización:** Permite guardar entidades relacionadas a nivel local sin depender del servidor.
*   **Orden temporal (Sortable):** A diferencia de UUIDv4, UUIDv7 incluye un timestamp, lo que mantiene la indexación (B-Tree) eficiente en PostgreSQL y evita el impacto en rendimiento por fragmentación de páginas.
*   **Agnóstico a la sincronización:** Elimina la necesidad de mapear "IDs temporales" de la tablet a "IDs definitivos" creados por PostGIS.

## Consequences
*   **Positive:** Sincronización offline nativa y fluida; mejora en inserción frente a UUIDv4.
*   **Negative:** Mayor consumo de almacenamiento por ID (16 bytes) frente a un integer/bigserial.

---

# ADR-002: Adopción del patrón Transactional Outbox para resiliencia de eventos

## Status
Accepted

## Context
La API (FastAPI) debe insertar datos geoespaciales en PostGIS y simultáneamente notificar a RabbitMQ respecto a la `inspeccion.creada` para que el Worker On-Premise actúe. Si enviamos a DB y luego falla RabbitMQ (Dual Write Problem), el Worker jamás descargará las fotos para generar el GIS on-premise, resultando en inconsistencia de la arquitectura.

## Decision
Implementar el patrón **Transactional Outbox**. FastAPI guardará los datos espaciales y el evento (en una tabla `outbox_events`) utilizando la **misma transacción** atómica de PostgreSQL. Un procesador asíncrono leerá de esta tabla y enrutará a RabbitMQ.

## Rationale
*   **Atomicidad (All-or-Nothing):** La base de datos asegura que la intención del evento queda registrada si y solo si la inserción espacial es exitosa.
*   **At-Least-Once Delivery:** Protege el ecosistema frente a caídas temporales del servidor RabbitMQ central.

## Consequences
*   **Positive:** Fuerte consistencia y total desacoplamiento de la disponibilidad inmediata de RabbitMQ desde el endpoint de consumo de la PWA.
*   **Negative:** Incrementa la carga transaccional de PostgreSQL y requiere el desarrollo de un servicio "Relay" o el uso de una herramienta Change Data Capture (CDC).
