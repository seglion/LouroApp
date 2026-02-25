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
- [ ] Desarrollo y verificación del motor **Sync Engine** background para encolar datos (JSON transaccional a la API FastAPI + MinIO Presigned URLs para imágenes).
- [ ] Pruebas unitarias y de simulación de conectividad "Offline/Online".
- [ ] Revisión de Calidad (Aplicación de `frontend-dev-guidelines` y `clean-code`).

## Revisión Final
- [ ] (A rellenar cuando las tareas estén completadas)
