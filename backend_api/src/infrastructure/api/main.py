from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.infrastructure.db.database import get_db

from src.infrastructure.api.schemas import InspeccionRequest
from src.domain.entities import Inspeccion, CoordenadasUTM, Acometida
from src.infrastructure.db.sqlalchemy_repository import SqlAlchemyInspeccionRepository
from src.application.register_inspeccion import RegisterInspeccionUseCase

app = FastAPI(
    title="API GIS Saneamiento - Field Collection",
    version="1.0.0",
    description="Backend microservice using Clean Architecture"
)

def get_register_inspeccion_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyInspeccionRepository(db)
    return RegisterInspeccionUseCase(repository)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Verifica el estado del servicio y la base de datos"""
    db_status = False
    try:
        # Check DB connection
        db.execute(text("SELECT 1"))
        db_status = True
    except Exception:
        db_status = False
        
    return {"status": "ok", "db_connected": db_status}

@app.post("/inspecciones", status_code=status.HTTP_201_CREATED)
def create_inspeccion(
    request: InspeccionRequest,
    use_case: RegisterInspeccionUseCase = Depends(get_register_inspeccion_use_case)
):
    acometidas_entities = [
        Acometida(
            id=ac.id,
            material=ac.material,
            diametro_mm=ac.diametro_mm,
            numero_acometida=ac.numero_acometida,
            profundidad_m=ac.profundidad_m
        ) for ac in request.acometidas
    ]

    inspeccion = Inspeccion(
        id=request.id,
        id_pozo=request.id_pozo,
        coordenadas_utm=CoordenadasUTM(x=request.coordenadas_utm.x, y=request.coordenadas_utm.y),
        tecnico_id=request.tecnico_id,
        fecha_inspec=request.fecha_inspec,
        calle_zona=request.calle_zona,
        situacion=request.situacion,
        cota_tapa=request.cota_tapa,
        profundidad_m=request.profundidad_m,
        estado=request.estado,
        material_pozo=request.material_pozo,
        tipo_acceso=request.tipo_acceso,
        num_pates=request.num_pates,
        forma_pozo=request.forma_pozo,
        diametro_pozo_mm=request.diametro_pozo_mm,
        largo_pozo_mm=request.largo_pozo_mm,
        ancho_pozo_mm=request.ancho_pozo_mm,
        resalto=request.resalto,
        filtraciones=request.filtraciones,
        pluviales=request.pluviales,
        biofilm=request.biofilm,
        tapa_forma=request.tapa_forma,
        tapa_tipo=request.tapa_tipo,
        tapa_material=request.tapa_material,
        tapa_diametro_mm=request.tapa_diametro_mm,
        tapa_largo_mm=request.tapa_largo_mm,
        tapa_ancho_mm=request.tapa_ancho_mm,
        red_tipo=request.red_tipo,
        red_viene_de_pozo=request.red_viene_de_pozo,
        red_va_a_pozo=request.red_va_a_pozo,
        red_carga=request.red_carga,
        colector_mat_entrada=request.colector_mat_entrada,
        colector_diametro_entrada_mm=request.colector_diametro_entrada_mm,
        colector_mat_salida=request.colector_mat_salida,
        colector_diametro_salida_mm=request.colector_diametro_salida_mm,
        ruta_foto_situacion=request.ruta_foto_situacion,
        ruta_foto_interior=request.ruta_foto_interior,
        observaciones=request.observaciones,
        acometidas=acometidas_entities
    )

    use_case.execute(inspeccion)
    return {"status": "created", "id": str(inspeccion.id)}

from uuid import UUID
from fastapi import HTTPException
from src.application.get_inspeccion import GetInspeccionUseCase
from src.application.update_inspeccion import UpdateInspeccionUseCase
from src.infrastructure.api.schemas import InspeccionUpdate

def get_get_inspeccion_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyInspeccionRepository(db)
    return GetInspeccionUseCase(repository)

def get_update_inspeccion_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyInspeccionRepository(db)
    return UpdateInspeccionUseCase(repository)

@app.get("/inspecciones/{inspeccion_id}")
def get_inspeccion(inspeccion_id: UUID, use_case: GetInspeccionUseCase = Depends(get_get_inspeccion_use_case)):
    inspeccion = use_case.get_by_id(inspeccion_id)
    if not inspeccion:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
    return inspeccion

@app.patch("/inspecciones/{inspeccion_id}")
def update_inspeccion(
    inspeccion_id: UUID, 
    request: InspeccionUpdate,
    get_use_case: GetInspeccionUseCase = Depends(get_get_inspeccion_use_case),
    update_use_case: UpdateInspeccionUseCase = Depends(get_update_inspeccion_use_case)
):
    current = get_use_case.get_by_id(inspeccion_id)
    if not current:
        raise HTTPException(status_code=404, detail="Inspección no encontrada")
        
    update_data = request.model_dump(exclude_unset=True)
    
    # Manejar relaciones y structs si vienen en el update
    if "acometidas" in update_data:
        current.acometidas = [
            Acometida(
                id=ac["id"],
                material=ac.get("material"),
                diametro_mm=ac.get("diametro_mm"),
                numero_acometida=ac.get("numero_acometida"),
                profundidad_m=ac.get("profundidad_m")
            ) for ac in update_data["acometidas"]
        ]
        del update_data["acometidas"]
        
    if "coordenadas_utm" in update_data:
        coords = update_data["coordenadas_utm"]
        current.coordenadas_utm = CoordenadasUTM(x=coords["x"], y=coords["y"])
        del update_data["coordenadas_utm"]

    # Actualizar los demás atributos
    for key, value in update_data.items():
        setattr(current, key, value)
        
    try:
        updated = update_use_case.execute(current)
        return {"status": "updated", "id": str(updated.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
