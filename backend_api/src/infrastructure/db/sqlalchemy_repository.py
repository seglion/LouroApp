import uuid
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities import Inspeccion, Acometida, CoordenadasUTM
from src.domain.repository_interface import InspeccionRepository
from src.infrastructure.db.models import PozoSaneamientoModel, AcometidaSaneamientoModel

class SqlAlchemyInspeccionRepository(InspeccionRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: PozoSaneamientoModel) -> Optional[Inspeccion]:
        if not model:
            return None
        
        from geoalchemy2.shape import to_shape
        shape = to_shape(model.geom)
        coords = CoordenadasUTM(x=shape.x, y=shape.y)
        
        acometidas_domain = [
            Acometida(
                id=ac.id,
                numero_acometida=ac.numero_acometida,
                material=ac.material,
                diametro_mm=ac.diametro_mm,
                profundidad_m=float(ac.profundidad_m) if ac.profundidad_m else None
            ) for ac in model.acometidas
        ]

        return Inspeccion(
            id=model.id,
            id_pozo=model.id_pozo,
            coordenadas_utm=coords,
            tecnico_id=model.tecnico_id,
            fecha_inspec=model.fecha_inspec,
            calle_zona=model.calle_zona,
            situacion=model.situacion,
            cota_tapa=float(model.cota_tapa) if model.cota_tapa else None,
            profundidad_m=float(model.profundidad_m) if model.profundidad_m else None,
            estado=model.estado,
            material_pozo=model.material_pozo,
            tipo_acceso=model.tipo_acceso,
            num_pates=model.num_pates,
            forma_pozo=model.forma_pozo,
            diametro_pozo_mm=model.diametro_pozo_mm,
            largo_pozo_mm=model.largo_pozo_mm,
            ancho_pozo_mm=model.ancho_pozo_mm,
            resalto=model.resalto,
            filtraciones=model.filtraciones,
            pluviales=model.pluviales,
            biofilm=model.biofilm,
            tapa_forma=model.tapa_forma,
            tapa_tipo=model.tapa_tipo,
            tapa_material=model.tapa_material,
            tapa_diametro_mm=model.tapa_diametro_mm,
            tapa_largo_mm=model.tapa_largo_mm,
            tapa_ancho_mm=model.tapa_ancho_mm,
            red_tipo=model.red_tipo,
            red_viene_de_pozo=model.red_viene_de_pozo,
            red_va_a_pozo=model.red_va_a_pozo,
            red_carga=model.red_carga,
            colector_mat_entrada=model.colector_mat_entrada,
            colector_diametro_entrada_mm=model.colector_diametro_entrada_mm,
            colector_mat_salida=model.colector_mat_salida,
            colector_diametro_salida_mm=model.colector_diametro_salida_mm,
            ruta_foto_situacion=model.ruta_foto_situacion,
            ruta_foto_interior=model.ruta_foto_interior,
            foto_keys=model.foto_keys or [],
            observaciones=model.observaciones,
            acometidas=acometidas_domain
        )

    def save(self, inspeccion: Inspeccion) -> None:
        wkt_geom = f"SRID=25829;POINT({inspeccion.coordenadas_utm.x} {inspeccion.coordenadas_utm.y})"

        pozo_model = PozoSaneamientoModel(
            id=inspeccion.id,
            id_pozo=inspeccion.id_pozo,
            geom=wkt_geom,
            tecnico_id=inspeccion.tecnico_id,
            fecha_inspec=inspeccion.fecha_inspec,
            calle_zona=inspeccion.calle_zona,
            situacion=inspeccion.situacion,
            cota_tapa=inspeccion.cota_tapa,
            profundidad_m=inspeccion.profundidad_m,
            estado=inspeccion.estado,
            material_pozo=inspeccion.material_pozo,
            tipo_acceso=inspeccion.tipo_acceso,
            num_pates=inspeccion.num_pates,
            forma_pozo=inspeccion.forma_pozo,
            diametro_pozo_mm=inspeccion.diametro_pozo_mm,
            largo_pozo_mm=inspeccion.largo_pozo_mm,
            ancho_pozo_mm=inspeccion.ancho_pozo_mm,
            resalto=inspeccion.resalto,
            filtraciones=inspeccion.filtraciones,
            pluviales=inspeccion.pluviales,
            biofilm=inspeccion.biofilm,
            tapa_forma=inspeccion.tapa_forma,
            tapa_tipo=inspeccion.tapa_tipo,
            tapa_material=inspeccion.tapa_material,
            tapa_diametro_mm=inspeccion.tapa_diametro_mm,
            tapa_largo_mm=inspeccion.tapa_largo_mm,
            tapa_ancho_mm=inspeccion.tapa_ancho_mm,
            red_tipo=inspeccion.red_tipo,
            red_viene_de_pozo=inspeccion.red_viene_de_pozo,
            red_va_a_pozo=inspeccion.red_va_a_pozo,
            red_carga=inspeccion.red_carga,
            colector_mat_entrada=inspeccion.colector_mat_entrada,
            colector_diametro_entrada_mm=inspeccion.colector_diametro_entrada_mm,
            colector_mat_salida=inspeccion.colector_mat_salida,
            colector_diametro_salida_mm=inspeccion.colector_diametro_salida_mm,
            ruta_foto_situacion=inspeccion.ruta_foto_situacion,
            ruta_foto_interior=inspeccion.ruta_foto_interior,
            foto_keys=inspeccion.foto_keys,
            observaciones=inspeccion.observaciones
        )

        for acometida in inspeccion.acometidas:
            acometida_model = AcometidaSaneamientoModel(
                id=acometida.id,
                numero_acometida=acometida.numero_acometida,
                material=acometida.material,
                diametro_mm=acometida.diametro_mm,
                profundidad_m=acometida.profundidad_m
            )
            pozo_model.acometidas.append(acometida_model)

        self.session.add(pozo_model)
        self.session.commit()

    def get_by_id(self, id: uuid.UUID) -> Optional[Inspeccion]:
        model = self.session.query(PozoSaneamientoModel).filter(PozoSaneamientoModel.id == id).first()
        return self._to_domain(model)

    def get_by_pozo_code(self, code: str) -> Optional[Inspeccion]:
        model = self.session.query(PozoSaneamientoModel).filter(PozoSaneamientoModel.id_pozo == code).first()
        return self._to_domain(model)

    def update(self, inspeccion: Inspeccion) -> None:
        model = self.session.query(PozoSaneamientoModel).filter(PozoSaneamientoModel.id == inspeccion.id).first()
        if not model:
            return

        wkt_geom = f"SRID=25829;POINT({inspeccion.coordenadas_utm.x} {inspeccion.coordenadas_utm.y})"
        model.geom = wkt_geom
        model.id_pozo = inspeccion.id_pozo
        model.tecnico_id = inspeccion.tecnico_id
        model.fecha_inspec = inspeccion.fecha_inspec
        model.calle_zona = inspeccion.calle_zona
        model.situacion = inspeccion.situacion
        model.cota_tapa = inspeccion.cota_tapa
        model.profundidad_m = inspeccion.profundidad_m
        model.estado = inspeccion.estado
        model.material_pozo = inspeccion.material_pozo
        model.tipo_acceso = inspeccion.tipo_acceso
        model.num_pates = inspeccion.num_pates
        model.forma_pozo = inspeccion.forma_pozo
        model.diametro_pozo_mm = inspeccion.diametro_pozo_mm
        model.largo_pozo_mm = inspeccion.largo_pozo_mm
        model.ancho_pozo_mm = inspeccion.ancho_pozo_mm
        model.resalto = inspeccion.resalto
        model.filtraciones = inspeccion.filtraciones
        model.pluviales = inspeccion.pluviales
        model.biofilm = inspeccion.biofilm
        model.tapa_forma = inspeccion.tapa_forma
        model.tapa_tipo = inspeccion.tapa_tipo
        model.tapa_material = inspeccion.tapa_material
        model.tapa_diametro_mm = inspeccion.tapa_diametro_mm
        model.tapa_largo_mm = inspeccion.tapa_largo_mm
        model.tapa_ancho_mm = inspeccion.tapa_ancho_mm
        model.red_tipo = inspeccion.red_tipo
        model.red_viene_de_pozo = inspeccion.red_viene_de_pozo
        model.red_va_a_pozo = inspeccion.red_va_a_pozo
        model.red_carga = inspeccion.red_carga
        model.colector_mat_entrada = inspeccion.colector_mat_entrada
        model.colector_diametro_entrada_mm = inspeccion.colector_diametro_entrada_mm
        model.colector_mat_salida = inspeccion.colector_mat_salida
        model.colector_diametro_salida_mm = inspeccion.colector_diametro_salida_mm
        model.ruta_foto_situacion = inspeccion.ruta_foto_situacion
        model.ruta_foto_interior = inspeccion.ruta_foto_interior
        model.foto_keys = inspeccion.foto_keys
        model.observaciones = inspeccion.observaciones

        # Actualizar relaciones Acometidas
        for ac in model.acometidas:
            self.session.delete(ac)
            
        new_acometidas = []
        for ac in inspeccion.acometidas:
            new_acometidas.append(
                AcometidaSaneamientoModel(
                    id=ac.id,
                    pozo_id=inspeccion.id,
                    numero_acometida=ac.numero_acometida,
                    material=ac.material,
                    diametro_mm=ac.diametro_mm,
                    profundidad_m=ac.profundidad_m
                )
            )
        model.acometidas = new_acometidas
        self.session.commit()
