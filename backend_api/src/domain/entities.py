import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class CoordenadasUTM:
    x: float
    y: float
    epsg: int = 25829

@dataclass
class Acometida:
    id: str
    material: Optional[str] = None
    diametro_mm: Optional[int] = None
    numero_acometida: Optional[int] = None
    profundidad_m: Optional[float] = None
    pos_reloj: Optional[str] = None

@dataclass
class RedEstructural:
    pos: str
    tipo: str
    material: str
    diametro_mm: int
    direccion_flujo: str

@dataclass
class Inspeccion:
    id: uuid.UUID
    id_pozo: str
    coordenadas_utm: CoordenadasUTM
    tecnico_id: Optional[uuid.UUID] = None
    fecha_inspec: Optional[date] = None
    calle_zona: Optional[str] = None
    situacion: Optional[str] = None
    cota_tapa: Optional[float] = None
    profundidad_m: Optional[float] = None
    estado: Optional[str] = None
    material_pozo: Optional[str] = None
    tipo_acceso: Optional[str] = None
    num_pates: Optional[int] = None
    forma_pozo: Optional[str] = None
    diametro_pozo_mm: Optional[int] = None
    largo_pozo_mm: Optional[int] = None
    ancho_pozo_mm: Optional[int] = None
    resalto: Optional[str] = None
    filtraciones: Optional[str] = None
    pluviales: Optional[str] = None
    biofilm: Optional[str] = None
    tapa_forma: Optional[str] = None
    tapa_tipo: Optional[str] = None
    tapa_material: Optional[str] = None
    tapa_diametro_mm: Optional[int] = None
    tapa_largo_mm: Optional[int] = None
    tapa_ancho_mm: Optional[int] = None
    red_tipo: Optional[str] = None
    red_viene_de_pozo: Optional[str] = None
    red_va_a_pozo: Optional[str] = None
    red_carga: Optional[str] = None
    colector_mat_entrada: Optional[str] = None
    colector_diametro_entrada_mm: Optional[int] = None
    colector_mat_salida: Optional[str] = None
    colector_diametro_salida_mm: Optional[int] = None
    ruta_foto_situacion: Optional[str] = None
    ruta_foto_interior: Optional[str] = None
    observaciones: Optional[str] = None
    foto_keys: list[str] = field(default_factory=list)
    acometidas: List[Acometida] = field(default_factory=list)
