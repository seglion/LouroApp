# Plan de Proyecto: Fase 4 (Mensajería y Desarrollo del Worker On-Premise)

## Hito 1: Preparación y Arquitectura del Worker (Docker & IAM)
- [x] Definir estructura del proyecto Python On-Premise (ej. `worker_on_premise/`).
- [x] Aplicar **Docker Expert**: Crear un `Dockerfile` optimizado (multi-stage) y `docker-compose.yml` seguro para el worker (usuario no root `appuser`, recursos limitados, control de capabilities).
- [x] Aplicar **AWS IAM Best Practices**: Definir y documentar políticas de mínimo privilegio (Least Privilege) para los accesos al bucket de MinIO (S3 compatible), inyectando credenciales vía AWS Secrets o variables de entorno.
- [x] Configurar el entorno virtual y esquema de dependencias (`pika`, `boto3`, `geopandas`, `fiona`, `sqlalchemy`).

## Hito 2: Consumo de Mensajería (RabbitMQ) y Resiliencia
- [x] Implementar cliente de RabbitMQ (usando `pika`) con reconexión robusta (connection recovery).
- [x] Configurar de consumo con **Acknowledgement manual (Ack/Nack)**.
- [x] Implementar control de **Idempotencia**: Base de datos SQLite local para registrar `event_id` y evitar procesamiento duplicado ante reentregas.

## Hito 3: Descarga Asíncrona e Integración MinIO
- [ ] Validar y extraer el payload del evento `inspeccion.creada`.
- [ ] Implementar cliente `boto3` apuntando a MinIO, implementando retries y descargas resilientes.
- [ ] Guardar las imágenes descargadas en el File System local (estructura: `Descargas_GIS/{Anio}/{Mes}/{Id_Pozo}/`).

## Hito 4: Generación y Actualización de Capas GIS (GeoPackage)
- [ ] Aplanar y formatear atributos extraídos del JSON (vinculando las rutas locales de las fotos).
- [ ] Usar `Fiona` / `GeoPandas` para abrir y/o crear un archivo `GeoPackage` (frente a Shapefile para mejor soporte de tipos).
- [ ] Insertar/Upsert de la métrica espacial (`Point` en EPSG:25829) y atributos, asegurando transaccionalidad local.

## Revisión Final y Documentación
- [ ] Levantar entorno de pruebas local (Rabbit + MinIO dockerizados) para E2E simulado.
- [ ] Verificación de seguridad y linting del worker (`flake8`, `bandit`).

---
<details>
<summary>Histórico Fase 3: Completada</summary>

# Plan de Proyecto: Reinicialización de la Fase 3 (Frontend PWA y Ecosistema Offline-First)

## Hito 1: Analítica y Preparación del Sistema de Diseño (Stitch)
- [x] Extraer y analizar en profundidad los HTML/CSS generados por el proyecto de Stitch (ID: 12549145011791967376) para aplicar las guías visuales.
- [x] Consolidar los tokens de diseño (Colores Utilitarios, Tipografía legible, Layouts orientados a Tablets) en la base del proyecto Vue.js, siguiendo las normativas de `frontend-design` y `ui-ux-pro-max`.
- [x] Reinicializar el proyecto Vue a estado inicial de Instalacion.
- [x] Implementar / Refactorizar la vista **Field Inspector Login**.
- [x] Implementar / Refactorizar la vista **Inspector Dashboard**, adaptándola exactamente a la funcionalidad requerida por Stitch (Nuevas inspecciones, sincronización y edición offline).

## Hito 2: Construcción del Sistema Multi-Paso (Formulario Dinámico)
- [x] Establecer un orquestador para el formulario multi-paso que preserve el estado en local (Pinia / sincronizado con rutas) entre las distintas páginas del asistentente.
- [x] **Paso 1:** Implementar vista "Ubicación y General".
- [x] **Paso 2:** Implementar vista "Detalles del Pozo".
- [x] **Paso 3:** Implementar vista "Detalles de la Tapa".
- [x] **Paso 4:** Implementar vista "Estado y Entorno".
- [x] **Paso 5:** Implementar vista "Red y Colector".
- [x] **Paso 6:** Implementar vista "Acometidas domiciliarias" (Soporte para listas dinámicas).

## Hito 3: Integración de Dispositivo y Persistencia Local
- [x] Integrar la **Geolocalización GPS** en el Paso 1, permitiendo adquirir las coordenadas del dispositivo en formato UTM ETRS89 Huso 29N dinámicamente.
- [x] Integrar captura interactiva **Fotográfica** de alta resolución (Situación / Interior) con previsualización en el Paso 4.
- [x] Definición robusta de datos en **IndexedDB** cumpliendo la jerarquía de `docs_arquitectura/openapi.yaml` (UUIDv7 offline, tabla Pozo, Acometidas y Metadatos de fotos).
- [x] Persistencia reactiva (auto-save) y recuperación de sesión tras recarga.

## Hito 4: Sincronización y Cierre
- [x] Desarrollo y verificación del motor **Sync Engine** background para encolar datos (JSON transaccional a la API FastAPI + MinIO Presigned URLs para imágenes).
- [x] Minitarea 1: Pruebas y simulación de conectividad "Offline/Online" (Verificar la cola de subida y recuperación de fallos).
- [x] Minitarea 2: Revisión de Calidad (Aplicación de `frontend-dev-guidelines` y `clean-code` en `sync.ts` y stores).
- [x] Minitarea 3: Limpieza y refactorización final (Organizar imports, asegurar tipado estricto y UX de estados de subida).

## Revisión Final
- [x] Verificación E2E de compilación, comprobación de tipos y linting (TypeScript y Vue TSC OK).
- [x] Redacción del `walkthrough.md` para empaquetado y cierre de fase.
</details>
