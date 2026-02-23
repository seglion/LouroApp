import pytest
import uuid
import random
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.user_entities import User, Role

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_test_user():
    db = SessionLocal()
    repository = SqlAlchemyUserRepository(db)
    
    user_id = uuid.uuid4()
    test_email = f"auth_{user_id}@test.com"
    test_password = "securePassword123"
    
    new_user = User(
        id=user_id,
        email=test_email,
        full_name="Usuario Auth Test",
        hashed_password=get_password_hash(test_password),
        role=Role.TECNICO
    )
    
    repository.save(new_user)
    db.close()
    
    return {
        "email": test_email,
        "password": test_password,
        "id": str(user_id)
    }

def test_login_wrong_password(setup_test_user):
    """Test 1: Intento de login con contraseña errónea (401)."""
    response = client.post("/login", data={
        "username": setup_test_user["email"],
        "password": "wrongPassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Email o contraseña incorrectos"

def test_login_success(setup_test_user):
    """Test 2: Login exitoso devuelve un token JWT."""
    response = client.post("/login", data={
        "username": setup_test_user["email"],
        "password": setup_test_user["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Save token for next tests
    setup_test_user["token"] = data["access_token"]

def test_create_inspeccion_without_token():
    """Test 3: Llamada a POST /inspecciones sin cabecera 'Authorization' (401)."""
    pozo_id = f"018f6d54-1b9a-7000-8000-0000{random.randint(10000000, 99999999)}"
    payload = {
        "id": pozo_id,
        "id_pozo": "P-NOAUTH",
        "coordenadas_utm": {"x": 100.0, "y": 200.0},
        "estado": "BUENO"
    }
    
    response = client.post("/inspecciones", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_inspeccion_with_token(setup_test_user):
    """Integración: Asegurar que con token válido se crea capturando el tecnico_id."""
    pozo_id = f"018f6d54-1ba0-7000-8000-0000{random.randint(10000000, 99999999)}"
    payload = {
        "id": pozo_id,
        "id_pozo": f"P-AUTH-{random.randint(1000, 9999)}",
        "coordenadas_utm": {"x": 100.0, "y": 200.0},
        "estado": "BUENO"
    }
    
    # Authorization Header required
    response = client.post(
        "/inspecciones", 
        json=payload,
        headers={"Authorization": f"Bearer {setup_test_user['token']}"}
    )
    assert response.status_code == 201
