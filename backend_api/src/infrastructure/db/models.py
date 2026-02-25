from sqlalchemy import Column, String, Float, Integer, ForeignKey, Date, Numeric, Text, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from src.infrastructure.db.database import Base

from src.domain.user_entities import Role

class UserModel(Base):
    __tablename__ = "tecnicos"  # Usamos la tabla especificada en 00_esquema_seguridad.sql

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nombre = Column("nombre", String(255), nullable=False) # Mapeo de full_name
    password_hash = Column("password_hash", String(255), nullable=False) # Mapeo de hashed_pwd
    rol = Column("rol", Enum(Role), nullable=False, default=Role.TECNICO) # Mapeo de role
    
    # Relación inversa (opcional pero recomendada para facilitar consultas)
    inspecciones = relationship("PozoSaneamientoModel", back_populates="tecnico")

class PozoSaneamientoModel(Base):
    __tablename__ = "pozos_saneamiento"

    id = Column(UUID(as_uuid=True), primary_key=True)
    id_pozo = Column(String(50), unique=True, nullable=False)
    geom = Column(Geometry('POINT', srid=25829))
    tecnico_id = Column(UUID(as_uuid=True), ForeignKey("tecnicos.id", ondelete="SET NULL"), nullable=True)
    fecha_inspec = Column(Date, nullable=True)
    calle_zona = Column(String(255))
    situacion = Column(String(255))
    cota_tapa = Column(Numeric(6, 2))
    profundidad_m = Column(Numeric(6, 2))
    estado = Column(String(50))
    material_pozo = Column(String(50))
    tipo_acceso = Column(String(50))
    num_pates = Column(Integer)
    forma_pozo = Column(String(50))
    diametro_pozo_mm = Column(Integer)
    largo_pozo_mm = Column(Integer)
    ancho_pozo_mm = Column(Integer)
    resalto = Column(String(50))
    filtraciones = Column(String(50))
    pluviales = Column(String(50))
    biofilm = Column(String(50))
    tapa_forma = Column(String(50))
    tapa_tipo = Column(String(50))
    tapa_material = Column(String(50))
    tapa_diametro_mm = Column(Integer)
    tapa_largo_mm = Column(Integer)
    tapa_ancho_mm = Column(Integer)
    red_tipo = Column(String(50))
    red_viene_de_pozo = Column(String(50))
    red_va_a_pozo = Column(String(50))
    red_carga = Column(String(50))
    colector_mat_entrada = Column(String(50))
    colector_diametro_entrada_mm = Column(Integer)
    colector_mat_salida = Column(String(50))
    colector_diametro_salida_mm = Column(Integer)
    ruta_foto_situacion = Column(String(255))
    ruta_foto_interior = Column(String(255))
    foto_keys = Column(ARRAY(String), default=list)
    observaciones = Column(Text)

    acometidas = relationship("AcometidaSaneamientoModel", back_populates="pozo", cascade="all, delete-orphan")
    tecnico = relationship("UserModel", back_populates="inspecciones")

class AcometidaSaneamientoModel(Base):
    __tablename__ = "acometidas_saneamiento"

    id = Column(UUID(as_uuid=True), primary_key=True)
    pozo_id = Column(UUID(as_uuid=True), ForeignKey("pozos_saneamiento.id", ondelete="CASCADE"), nullable=False)
    numero_acometida = Column(Integer)
    material = Column(String(50))
    diametro_mm = Column(Integer)
    profundidad_m = Column(Numeric(5, 2))

    pozo = relationship("PozoSaneamientoModel", back_populates="acometidas")
