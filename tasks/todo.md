# Plan de Acción: Herencia de datos del pozo anterior

## Análisis y Diseño
- [ ] Investigar en `src/store/inspeccion.ts` cómo obtener la última inspección (sincronizada o pendiente) desde IndexedDB.
- [ ] Definir los campos que deben "heredarse" o tener nuevos valores predeterminados.

## Implementación
- [x] **DB:** Añadir `finalizada` a los índices para optimizar búsquedas.
- [x] **Store:** Modificar `iniciarNuevaInspeccion` para intentar cargar datos de la última inspección realizada (sincronizada o lista para sincronizar).
- [x] **Paso 1 (Ubicación):**
    - [x] Preseleccionar `situacion` del pozo anterior.
- [x] **Paso 2 (Tapa):**
    - [x] Preseleccionar `tapa_forma` del pozo anterior (Default: 'Circular').
    - [x] Preseleccionar `tapa_diametro_mm` si es circular (Default: 600).
    - [x] Preseleccionar `tapa_material` (Default: 'Fundición Dúctil').
    - [x] Preseleccionar `tapa_tipo` (Default: 'Abatible').
- [x] **Paso 3 (Pozo):**
    - [x] Preseleccionar `forma_pozo`, `material_pozo` y dimensiones del pozo anterior.
    - [x] Default `diametro_pozo_mm`: 1000.
    - [x] Default `tipo_acceso`: 'Ninguno'.

## Verificación
- [ ] Crear una inspección, completarla, y verificar que la siguiente herede los valores indicados.
- [ ] Verificar que si no hay inspección previa, se usen los nuevos valores por defecto (600mm, etc).
