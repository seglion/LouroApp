| Paso Stitch | Campo UI | Columna DB / Interface TS | Tipo |
| :--- | :--- | :--- | :--- |
| 1: Location | Manhole ID | `id_pozo` | string |
| 1: Location | Project Name | `project_name` | string |
| 1: Location | Inspector Name | `inspector_name` | string |
| 1: Location | Date | `fecha_inspec` | string (ISO) |
| 2: Dimensions | Cover Material | `tapa_material` | Enum |
| 2: Dimensions | Cover Shape | `tapa_forma` | Enum |
| 2: Dimensions | Width/Diam (mm) | `tapa_diametro_mm` | number |
| 2: Dimensions | Depth (m) | `profundidad_m` | number |
| 3: Condition | Fractures Severity | `fracturas_sev` | number (1-5) |
| 3: Condition | Leaks Severity | `filtraciones_sev` | number (1-5) |
| 3: Condition | Biofilm Severity | `biofilm_sev` | number (1-5) |
| 3: Condition | Corrosion Severity| `corrosion_sev` | number (1-5) |
| 4: Pipe Network | Position (Clock) | `red_estructural[].pos` | string |
| 4: Pipe Network | Type (In/Out) | `red_estructural[].tipo` | string |
| 5: House Conn | Connection ID | `acometidas[].id` | string |
| 5: House Conn | Depth (m) | `acometidas[].prof` | number |
