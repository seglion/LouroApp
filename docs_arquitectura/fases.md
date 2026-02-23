Plan de Proyecto: Plataforma Híbrida de Recolección de Datos GIS
Fase 0: Definición de Arquitectura, Modelado y ADRs
Antes de tocar infraestructura, debemos formalizar los contratos y políticas de sincronización para evitar acoplamiento y problemas de concurrencia.

Objetivos principales: Documentar decisiones críticas mediante Architecture Decision Records (ADRs), definir contratos de API y modelar la sincronización offline-first.
Hitos / Entregables:
Hito 0.1: Repositorio de ADRs creado (aprobados: Estrategia de IDs, Patrón transaccional, Resolución de conflictos offline).
Hito 0.2: Contratos de API (OpenAPI/Swagger) y payload de eventos en RabbitMQ definidos.
Hito 0.3: Diseño del modelo de datos GIS (PostGIS schema y EPSG:25829 aplicado a las tablas geospaciales).
Riesgos Técnicos y Mitigación:
Riesgo: Conflictos en la generación de IDs offline.
Mitigación: Adoptar UUIDv7 (ordenables por tiempo) generados en el frontend (PWA) al instante de capturar el dato. El backend nunca genera IDs primarios de negocio; solo valida.
Fase 1: Infraestructura Cloud y On-Premise (Fundamentos)
Establecer el terreno de juego con infraestructura como código (IaC), garantizando entornos idénticos (Dev, Staging, Prod).

Objetivos principales: Desplegar el clúster dockerizado en Hetzner y preparar el servidor on-premise, configurando redes, seguridad (TLS/SSL) y monitoreo base.
Hitos / Entregables:
Hito 1.1: Servidor Hetzner aprovisionado con Docker Engine/Swarm o k3s.
Hito 1.2: Base de datos (PostgreSQL + PostGIS), MinIO y RabbitMQ desplegados y securizados en la nube.
Hito 1.3: Conexión VPN/TLS configurada de forma segura para el Worker On-Premise.
Orden de ejecución: 1) Cloud networking/seguridad -> 2) Despliegue de servicios middleware (DB, MQ, Storage) -> 3) Pruebas de conectividad desde On-Premise.




Fase 2: Desarrollo del Backend Cloud (FastAPI)
Construir la capa de servicios REST que interactuará con la PWA.

Objetivos principales: Implementar la API de ingesta de datos, subida de imágenes (presigned URLs en MinIO) y publicación de eventos hacia RabbitMQ.
Hitos / Entregables:
Hito 2.1: Endpoints de catálogos y referencias (datos "read-only" para la PWA).
Hito 2.2: Implementación Transaccional de ingesta: POST /inspeccion (guarda en PostGIS y emite evento a RabbitMQ).
Hito 2.3: Integración de MinIO mediante Presigned URLs para desacoplar el tráfico pesado de la aplicación de la API de FastAPI.
Riesgos Técnicos y Mitigación:
Riesgo (Transacciones Distribuidas): El registro se guarda en PostGIS, pero RabbitMQ falla al recibir el evento (Dual Write Problem).
Mitigación: Implementar el Transactional Outbox Pattern. FastAPI guarda el dato GIS y el evento en una tabla "outbox" de PostgreSQL en la misma transacción. Un proceso en background (o CDC) lee el outbox y lo envía a RabbitMQ, garantizando entrega At-Least-Once.








Fase 3: Frontend PWA y Ecosistema Offline-First (Vue.js)
El componente más crítico de cara al usuario. Debe sentirse como una aplicación nativa.

Objetivos principales: Construir los formularios complejos en Vue.js, integrar captura hardware e implementar la persistencia local de datos y cola de envíos.
Hitos / Entregables:
Hito 3.1: Configuración de Service Workers e IndexedDB (ej. usando localForage o Dexie.js).
Hito 3.2: Formularios dinámicos con validación local y captura de GPS (precisión y transformación si es requerida por el visualizador de la tablet, aunque PostGIS mantendrá el EPSG:25829 interno).
Hito 3.3: Captura de fotos de alta resolución y almacenamiento optimizado en dispositivo local.
Hito 3.4: "Sync Engine": Motor background en la PWA que encola y gestiona la subida cuando recupera 4G/Wifi.
Riesgos Técnicos y Mitigación:
Riesgo (Conflictos Offline y "Lost Updates"): Dos técnicos inspeccionando o modificando el mismo pozo simultáneamente en zonas sin cobertura.
Mitigación: Usar control de concurrencia optimista (Versionado / ETags) sumado a un modelo de tipo Event Sourcing ligero o "Append Only" para las inspecciones. En una inspección física el riesgo de pisarse es menor, pero las tablas deben aceptar deltas de información en vez de un "upsert" ciego.
Riesgo: Sincronización bloqueada por una foto corrupta o hiper-pesada.
Mitigación: Subir metadatos (JSON) primero, subir fotos después (vía Presigned URLs directos a MinIO). El backend junta el estado final usando eventos.
Fase 4: Mensajería y Desarrollo del Worker On-Premise
Conteo e integración del flujo desde la nube hasta la oficina técnica.

Objetivos principales: Programar el orquestador on-premise que escuche la cola e inserte la información GIS final localmente.
Hitos / Entregables:
Hito 4.1: Script Python consumiendo de RabbitMQ con reconexión robusta (Acknowledgement manual).
Hito 4.2: Descarga asíncrona de MinIO y organización en el File System local (Rutas estructuradas por Provincia/Fecha/ID).
Hito 4.3: Generación/Actualización de capas (Shapefile/GeoPackage) usando Fiona/GeoPandas.
Riesgos Técnicos y Mitigación:
Riesgo (Idempotencia en el Worker): Como aseguramos At-Least-Once delivery, el worker puede recibir el mismo evento dos veces.
Mitigación: El Worker On-Premise debe ser diseñado para ser idempotente. Cada Worker debe mantener un registro local (ej. una pequeña DB SQLite local) de evento_id procesados. Si un archivo o registro ya existe para ese UUID, actualiza o simplemente hace ack e ignora.
Fase 5: Pruebas End-to-End (E2E) y "Field Testing" (Pruebas de Campo)
Validación en condiciones extremas y de mundo real.

Objetivos principales: Romper el sistema controladamente ("Chaos Engineering" pasivo) y validar usabilidad y flujos transaccionales puros.
Hitos / Entregables:
Hito 5.1: Pruebas Unitarias e Integración CI/CD (aprobadas).
Hito 5.2: Simulación E2E de "Cobertura Intermitente" (Usando throttling de Chrome/Tablets para simular 2G/pérdida de red).
Hito 5.3: Field Testing real (Prueba piloto): 2 técnicos durante 3 días levantando datos reales con las tablets con cobertura real fluctuante.
Secuencia Lógica: Tests unitarios de sincronización -> Simulación de red en laboratorio -> Prueba piloto en la calle.
Fase 6: Despliegue, Monitorización Activa y Paso a Producción
Lanzamiento formal controlando la degradación y observabilidad.

Objetivos principales: Despliegue formal en producción, entrega a los usuarios finales y activación de alertas.
Hitos / Entregables:
Hito 6.1: Tableros de monitorización (Grafana/Prometheus) y Logs centralizados (promedio de DB locks, RabbitMQ queue length).
Hito 6.2: "Dead Letter Queues" (DLQ) configuradas en RabbitMQ con estrategia de reprocesado para fallos on-premise (ej. disco lleno en servidor físico).
Hito 6.3: Capacitación a equipo de GIS y técnicos de campo.
Estrategia de Mitigación de Producción: Activar monitoreo sobre el volumen de la tabla Outbox del backend FastAPI y la longitud de colas en RabbitMQ. Si crecen sin parar, es síntoma temprano de que el esquema On-Premise ha perdido conexión.
Resumen de Patrones Arquitectónicos Aplicados en este Plan:
Offline-first con UUIDv7: Resuelve cuellos de botella de red al descentralizar la creación de IDs (Skill: Architecture Patterns).
Transactional Outbox Pattern: Asegura que los datos GIS en PostgreSQL y los Eventos en RabbitMQ nunca queden inconsistentes (Skill: Microservices Patterns / Event Sourcing).
Coreografía Mediante Eventos y Presigned URLs: Desacopla la API de FastAPI de la manipulación pesada de imágenes y unifica al entorno On-Premise (Skill: Senior Architect).
Consumidor Idempotente On-Premise: Permite reintentos seguros (Acks / Nacks) desde la cola RabbitMQ sin corromper la planimetría de Shapefiles/Geopackages.