# Lecciones Aprendidas

- **Arquitectura**: Nunca ignores o diluyas decisiones arquitectónicas previas (ADRs) al escribir tests. Según el `ADR-001`, la PWA usa UUIDv7 para gestionar localmente la creación de las Ids antes de enviar al backend. Por tanto, los **Payloads simulados en TDD siempre deben inyectar una estructura idéntica (ej: Strings UUIDv7 duros)** y no depender de métodos genéricos de Python (`uuid4()`), para asegurar la congruencia y el realismo entre componentes offline-first y el microservicio.
