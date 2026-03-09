# Plan de Acción: Validación de Cota Obligatoria

## Análisis y Diseño
- [x] Rastrear la validez del Paso 1 en la interfaz gráfica (botón Siguiente).
- [x] Localizar el getter `pasoActualValido` en `src/store/inspeccion.ts`.

## Implementación
- [x] **Paso 1 (Store):** Modificar el `case 1:` del getter en `inspeccion.ts`.
- [x] **Paso 1 (Store):** Añadir validación técnica tipo `i.cota_tapa !== null && i.cota_tapa !== undefined && i.cota_tapa !== ''`.

## Revisión Final
- [x] Comprobar que el botón Siguiente del footer queda inhabilitado si la cota Z está en blanco.
- [x] Comprobar que se permite pasar si la cota Z es 0.
