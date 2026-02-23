import uuid
import random
import pytest
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.models import PozoSaneamientoModel
from src.infrastructure.api.dependencies import get_current_user
from src.domain.user_entities import User, Role
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository

TEST_TECNICO = None

def mock_get_current_user():
    return TEST_TECNICO

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def setup_tecnico():
    global TEST_TECNICO
    db = SessionLocal()
    repo = SqlAlchemyUserRepository(db)
    
    uid = uuid.uuid4()
    TEST_TECNICO = User(
        id=uid,
        email=f"tester_{uid}@test.com",
        full_name="Tester",
        hashed_password="pwd",
        role=Role.TECNICO
    )
    repo.save(TEST_TECNICO)
    db.close()

def test_register_inspeccion_success():
    """Test para validar TDD: Creación de Inspección Completa"""
    # Simulamos UUIDv7 válidos generados desde la PWA según el ADR-001 (randomizados para no chocar)
    pozo_id = f"018f6d54-1b9a-7000-8000-0000{random.randint(10000000, 99999999)}"
    acometida_id = f"018f6d54-1b9a-7000-8000-0000{random.randint(10000000, 99999999)}"
    id_pozo_real = f"P-{random.randint(1000, 99999)}"

    payload = {
        "id": pozo_id,
        "id_pozo": id_pozo_real,
        "coordenadas_utm": {
            "x": 535492.31,
            "y": 4801123.54
        },
        "fecha_inspec": "2026-02-23",
        "calle_zona": "Av. Principal",
        "situacion": "Calzada",
        "cota_tapa": 12.345,
        "profundidad_m": 2.10,
        "estado": "BUENO",
        "material_pozo": "HORMIGON",
        "tipo_acceso": "LIBRE",
        "num_pates": 5,
        "forma_pozo": "CIRCULAR",
        "diametro_pozo_mm": 1000,
        "tapa_forma": "CIRCULAR",
        "tapa_tipo": "ABISAGRADA",
        "tapa_material": "FUNDICION",
        "tapa_diametro_mm": 600,
        "red_tipo": "SANEAMIENTO",
        "colector_mat_entrada": "PVC",
        "colector_diametro_entrada_mm": 315,
        "colector_mat_salida": "PVC",
        "colector_diametro_salida_mm": 400,
        "ruta_foto_situacion": "s3://gis-captures/pozos/test_sit.jpg",
        "ruta_foto_interior": "s3://gis-captures/pozos/test_int.jpg",
        "observaciones": "Test integration TDD",
        "acometidas": [
            {
                "id": acometida_id,
                "numero_acometida": 1,
                "material": "PVC",
                "diametro_mm": 200,
                "profundidad_m": 1.25
            }
        ]
    }

    response = client.post("/inspecciones", json=payload)
    
    assert response.status_code == 201
    assert response.json() == {"status": "created", "id": pozo_id}

    db = SessionLocal()
    pozo = db.query(PozoSaneamientoModel).filter(PozoSaneamientoModel.id == pozo_id).first()
    assert pozo is not None
    assert pozo.id_pozo == id_pozo_real
    assert len(pozo.acometidas) == 1
    db.close()
