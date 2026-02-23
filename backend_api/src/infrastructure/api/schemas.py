from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from uuid import UUID

class CoordenadasUTMBase(BaseModel):
    x: float = Field(..., description="Este (Easting) en metros")
    y: float = Field(..., description="Norte (Northing) en metros")

class AcometidaData(BaseModel):
    id: UUID
    numero_acometida: int
    material: Optional[str] = Field(None, max_length=50)
    diametro_mm: Optional[int] = None
    profundidad_m: Optional[float] = None

class InspeccionRequest(BaseModel):
    id: UUID
    id_pozo: str = Field(..., max_length=50)
    coordenadas_utm: CoordenadasUTMBase
    fecha_inspec: Optional[date] = None
    calle_zona: Optional[str] = Field(None, max_length=255)
    situacion: Optional[str] = Field(None, max_length=100)
    cota_tapa: Optional[float] = None
    profundidad_m: Optional[float] = None
    estado: Optional[str] = Field(None, max_length=50)
    material_pozo: Optional[str] = Field(None, max_length=50)
    tipo_acceso: Optional[str] = Field(None, max_length=50)
    num_pates: Optional[int] = None
    forma_pozo: Optional[str] = Field(None, max_length=50)
    diametro_pozo_mm: Optional[int] = None
    largo_pozo_mm: Optional[int] = None
    ancho_pozo_mm: Optional[int] = None
    resalto: Optional[str] = Field(None, max_length=50)
    filtraciones: Optional[str] = Field(None, max_length=50)
    pluviales: Optional[str] = Field(None, max_length=50)
    biofilm: Optional[str] = Field(None, max_length=50)
    tapa_forma: Optional[str] = Field(None, max_length=50)
    tapa_tipo: Optional[str] = Field(None, max_length=50)
    tapa_material: Optional[str] = Field(None, max_length=50)
    tapa_diametro_mm: Optional[int] = None
    tapa_largo_mm: Optional[int] = None
    tapa_ancho_mm: Optional[int] = None
    red_tipo: Optional[str] = Field(None, max_length=50)
    red_viene_de_pozo: Optional[str] = Field(None, max_length=50)
    red_va_a_pozo: Optional[str] = Field(None, max_length=50)
    red_carga: Optional[str] = Field(None, max_length=50)
    colector_mat_entrada: Optional[str] = Field(None, max_length=50)
    colector_diametro_entrada_mm: Optional[int] = None
    colector_mat_salida: Optional[str] = Field(None, max_length=50)
    colector_diametro_salida_mm: Optional[int] = None
    ruta_foto_situacion: Optional[str] = None
    ruta_foto_interior: Optional[str] = None
    observaciones: Optional[str] = None
    acometidas: List[AcometidaData] = Field(default_factory=list)

class InspeccionUpdate(BaseModel):
    id_pozo: Optional[str] = Field(None, max_length=50)
    coordenadas_utm: Optional[CoordenadasUTMBase] = None
    tecnico_id: Optional[UUID] = None
    fecha_inspec: Optional[date] = None
    calle_zona: Optional[str] = Field(None, max_length=255)
    situacion: Optional[str] = Field(None, max_length=100)
    cota_tapa: Optional[float] = None
    profundidad_m: Optional[float] = None
    estado: Optional[str] = Field(None, max_length=50)
    material_pozo: Optional[str] = Field(None, max_length=50)
    tipo_acceso: Optional[str] = Field(None, max_length=50)
    num_pates: Optional[int] = None
    forma_pozo: Optional[str] = Field(None, max_length=50)
    diametro_pozo_mm: Optional[int] = None
    largo_pozo_mm: Optional[int] = None
    ancho_pozo_mm: Optional[int] = None
    resalto: Optional[str] = Field(None, max_length=50)
    filtraciones: Optional[str] = Field(None, max_length=50)
    pluviales: Optional[str] = Field(None, max_length=50)
    biofilm: Optional[str] = Field(None, max_length=50)
    tapa_forma: Optional[str] = Field(None, max_length=50)
    tapa_tipo: Optional[str] = Field(None, max_length=50)
    tapa_material: Optional[str] = Field(None, max_length=50)
    tapa_diametro_mm: Optional[int] = None
    tapa_largo_mm: Optional[int] = None
    tapa_ancho_mm: Optional[int] = None
    red_tipo: Optional[str] = Field(None, max_length=50)
    red_viene_de_pozo: Optional[str] = Field(None, max_length=50)
    red_va_a_pozo: Optional[str] = Field(None, max_length=50)
    red_carga: Optional[str] = Field(None, max_length=50)
    colector_mat_entrada: Optional[str] = Field(None, max_length=50)
    colector_diametro_entrada_mm: Optional[int] = None
    colector_mat_salida: Optional[str] = Field(None, max_length=50)
    colector_diametro_salida_mm: Optional[int] = None
    ruta_foto_situacion: Optional[str] = None
    ruta_foto_interior: Optional[str] = None
    observaciones: Optional[str] = None
    acometidas: Optional[List[AcometidaData]] = None
