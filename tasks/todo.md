# Plan de Acción: Integración de Inventario Geoespacial (Radar de Pozos)

## Análisis y Diseño (Frontend Design)
- **Concepto**: "Radar de Activos Cercanos". El operario ve automáticamente los pozos en un radio de 100m.
- **A estética**: Industrial Utilitarian. Marcadores precisos, círculos de radio técnicos.
- **Diferenciación**: Selección interactiva desde mapa para evitar errores de escritura en IDs.

## Tareas
- [x] **Datos Mock**: Crear un set de datos de ejemplo (Pozos) cerca de las coordenadas de trabajo habituales.
- [x] **Lógica Espacial**: Implementar filtro de proximidad (distancia Euclídea en UTM).
- [x] **Componente Mapa (`Paso1_General.vue`)**:
    - [x] Añadir capa de "Radar" (Círculo de 100m alrededor del GPS).
    - [x] Añadir capa de "Pozos Cercanos" con iconos diferenciados.
    - [x] Implementar evento `click` en los pozos para capturar el `id_pozo`.
- [x] **Estilo**: Asegurar que los marcadores y el radar se integren con el diseño premium/industrial.

## Verificación
- [ ] Simular captura de GPS y comprobar que aparecen puntos cercanos.
- [ ] Hacer clic en un punto y verificar que el campo `ID del Activo` se rellena solo.
