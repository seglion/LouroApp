from fastapi import FastAPI, Depends, status, HTTPException, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.infrastructure.db.database import Base, engine, get_db
from src.infrastructure.db.sqlalchemy_repository import SqlAlchemyInspeccionRepository
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.application.register_inspeccion import RegisterInspeccionUseCase
from src.application.login_user import LoginUserUseCase
from src.infrastructure.api.dependencies import get_current_user
from src.domain.policies import ForbiddenError
from src.domain.entities import Inspeccion, CoordenadasUTM, Acometida
from src.domain.user_entities import User, Role
from src.infrastructure.api.schemas import InspeccionRequest, InspeccionUpdate, UserUpdate
from pydantic import BaseModel, Field, EmailStr
from src.application.update_user import UpdateUserUseCase
from src.application.create_user import CreateUserUseCase
import uuid
from src.application.upload_inspeccion_foto import UploadInspeccionFotoUseCase
from src.infrastructure.storage.minio_client import MinioStorageClient

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=100)
    role: Role


# ... Create tables (just in case) ...
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LouroApp API", version="1.0.0")

@app.exception_handler(ForbiddenError)
async def forbidden_exception_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

def get_update_user_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyUserRepository(db)
    return UpdateUserUseCase(repository)

@app.patch("/users/me")
def update_profile(
    request: UserUpdate,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
    current_user: User = Depends(get_current_user)
):
    try:
         # Pydantic nos dará None si el campo no se envio gracias a todos los fields de update opcionales.
         use_case.execute(
             target_user=current_user,
             current_user=current_user,
             full_name=request.full_name,
             email=request.email,
             new_password=request.password
         )
         return {"message": "Perfil actualizado correctamente"}
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))

def get_create_user_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyUserRepository(db)
    return CreateUserUseCase(repository)

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreate,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    current_user: User = Depends(get_current_user)
):
    try:
        new_user = use_case.execute(
            current_user=current_user,
            email=request.email,
            full_name=request.full_name,
            password=request.password,
            role=request.role
        )
        return {"id": str(new_user.id), "email": new_user.email, "role": new_user.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_login_use_case(db: Session = Depends(get_db)):
    repository = SqlAlchemyUserRepository(db)
    return LoginUserUseCase(repository)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), use_case: LoginUserUseCase = Depends(get_login_use_case)):
    token = use_case.execute(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}

from src.domain.event_publisher_interface import EventPublisher
from src.infrastructure.events.rabbitmq_publisher import RabbitMQPublisher

def get_event_publisher():
    # Devuelve la configuración de producción real a RabbitMQ
    return RabbitMQPublisher(host="gis_saneamiento_rabbit", exchange="inspecciones.v1")

def get_register_inspeccion_use_case(db: Session = Depends(get_db), publisher: EventPublisher = Depends(get_event_publisher)):
    repository = SqlAlchemyInspeccionRepository(db)
    user_repo = SqlAlchemyUserRepository(db)
    return RegisterInspeccionUseCase(repository, user_repo=user_repo, event_publisher=publisher)

def get_minio_client():
    return MinioStorageClient()

def get_upload_inspeccion_foto_use_case(
    db: Session = Depends(get_db),
    storage: MinioStorageClient = Depends(get_minio_client)
):
    repository = SqlAlchemyInspeccionRepository(db)
    return UploadInspeccionFotoUseCase(repository, storage)

@app.post("/inspecciones/{inspeccion_id}/photos", status_code=status.HTTP_201_CREATED)
def upload_foto(
    inspeccion_id: uuid.UUID,
    file: UploadFile = File(...),
    use_case: UploadInspeccionFotoUseCase = Depends(get_upload_inspeccion_foto_use_case),
    current_user: User = Depends(get_current_user)
):
    try:
        new_keys = use_case.execute(
            inspeccion_id=inspeccion_id,
            file_data=file.file,
            file_name=file.filename,
            content_type=file.content_type,
            current_user=current_user
        )
        return {"status": "success", "foto_keys": new_keys}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    # Domain ForbiddenError is already natively handled by exception_handler

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
    use_case: RegisterInspeccionUseCase = Depends(get_register_inspeccion_use_case),
    current_user: User = Depends(get_current_user)
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
    coords = CoordenadasUTM(x=request.coordenadas_utm.x, y=request.coordenadas_utm.y)

    inspeccion = Inspeccion(
        id=request.id,
        id_pozo=request.id_pozo,
        coordenadas_utm=coords,
        tecnico_id=current_user.id,
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
    update_use_case: UpdateInspeccionUseCase = Depends(get_update_inspeccion_use_case),
    current_user: User = Depends(get_current_user)
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
        updated = update_use_case.execute(current, current_user)
        return {"status": "updated", "id": str(updated.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
