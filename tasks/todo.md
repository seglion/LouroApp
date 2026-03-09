# Plan de Acción: Refinamiento Paso 2 (Acceso y Materiales)

## Análisis y Diseño
- [x] Identificar la lista de opciones de "Sistema de Acceso" en `Paso2_Detalles.vue`.
- [x] Localizar el estado inicial en `src/store/inspeccion.ts`.

## Implementación
- [x] **Store:** Cambiar el valor inicial de `material_pozo` a 'Hormigón' en `getInitialState`.
- [x] **Paso 2 (Detalles):** Eliminar la opción 'Pates' del array de botones de "Sistema de Acceso".
- [x] **Paso 2 (Detalles):** Verificar que la lógica subordinada (cantidad de peldaños) siga funcionando correctamente para otras opciones.

## Revisión Final
- [x] Validar que una nueva inspección comience con "Hormigón" ya seleccionado.
- [x] Comprobar que el botón "Pates" ya no aparece en la interfaz.
- [x] Realizar commit con los cambios.
