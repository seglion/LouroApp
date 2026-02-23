import uuid
import random
import pytest
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.api.dependencies import get_current_user
from src.domain.user_entities import User, Role
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.db.database import SessionLocal

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

def test_full_inspeccion_lifecycle():
    # 1. Crear una inspección ("mock" de UUIDv7 válidos)
    pozo_id = f"018f6d54-1b9a-7000-8000-000000000{random.randint(100, 999)}"
    acometida_id = f"018f6d54-1b9b-7000-8000-000000000{random.randint(100, 999)}"
    id_pozo_real = f"P-TEST-{random.randint(1000, 99999)}"

    create_payload = {
        "id": pozo_id,
        "id_pozo": id_pozo_real,
        "coordenadas_utm": {"x": 100.0, "y": 200.0},
        "estado": "BUENO",
        "diametro_pozo_mm": 1000,
        "acometidas": [
            {
                "id": acometida_id,
                "numero_acometida": 1,
                "diametro_mm": 200
            }
        ]
    }

    create_res = client.post("/inspecciones", json=create_payload)
    assert create_res.status_code == 201

    # 2. Get por ID y verificar (Test 1)
    get_res = client.get(f"/inspecciones/{pozo_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id_pozo"] == id_pozo_real
    assert data["diametro_pozo_mm"] == 1000
    assert len(data["acometidas"]) == 1
    assert data["acometidas"][0]["diametro_mm"] == 200

    # 3. Update el diametro y añadir estado VALIDADA (Test 2)
    update_payload = {
        "diametro_pozo_mm": 1200,
        "estado": "VALIDADA"
    }
    update_res = client.patch(f"/inspecciones/{pozo_id}", json=update_payload)
    assert update_res.status_code == 200

    # Verificar que el update se guardó 
    get_res2 = client.get(f"/inspecciones/{pozo_id}")
    data2 = get_res2.json()
    assert data2["diametro_pozo_mm"] == 1200
    assert data2["estado"] == "VALIDADA"

    # 4. Intentar actualizar de nuevo (Debería fallar por la regla de negocio)
    fail_payload = {
        "diametro_pozo_mm": 1500
    }
    fail_res = client.patch(f"/inspecciones/{pozo_id}", json=fail_payload)
    assert fail_res.status_code == 400
    assert "no se puede editar" in fail_res.json()["detail"].lower()
