# Tareas: Tipo de Cierre y Foto de Esquema (PRODUCCIÓN)

## Migraciones de Datos
- [x] Ejecutar el siguiente script SQL en la base de datos de producción (PostgreSQL):
  ```sql
  ALTER TABLE pozos_saneamiento 
    ADD COLUMN red_viene_de_pozo_2 VARCHAR(50),
    ADD COLUMN red_va_a_pozo_2 VARCHAR(50),
    ADD COLUMN colector_mat_entrada_2 VARCHAR(50),
    ADD COLUMN colector_diametro_entrada_mm_2 INTEGER,
    ADD COLUMN colector_mat_salida_2 VARCHAR(50),
    ADD COLUMN colector_diametro_salida_mm_2 INTEGER,
    ADD COLUMN ruta_foto_esquema TEXT;
  ```
- [ ] Incrementar versión a **3** en `src/db/db.ts` (IndexedDB)

## Backend (API)
- [x] Actualizar entidad de dominio en `src/domain/entities.py`
- [x] Actualizar modelo de base de datos en `src/infrastructure/db/models.py`
- [x] Actualizar esquemas de Pydantic en `src/infrastructure/api/schemas.py`
- [x] Actualizar lógica de creación/actualización en `src/infrastructure/api/main.py`
- [x] Actualizar script de inicialización `01_init_schema.sql`

## Worker On-Premise
- [ ] Modificar `main.py` para detectar sufijo `_esquema` en fotos
- [ ] Añadir campo `ruta_foto_esquema` al esquema de GeoPackage

## Frontend (PWA)
- [ ] Actualizar interfaces y tipos en `src/db/db.ts`
- [ ] Actualizar el store de Pinia `src/store/inspeccion.ts`
- [ ] Añadir opción "Normal" en `src/views/inspeccion/Paso3_Tapa.vue`
- [ ] Implementar captura de foto "Esquema" en `src/views/inspeccion/Paso2_Detalles.vue`

## Verificación
- [ ] Probar persistencia local (IndexedDB)
- [ ] Verificar descarga de fotos en el Worker
- [ ] Confirmar generación de nueva columna en GeoPackage
