import pytest
import uuid
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.user_entities import User, Role

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_update_user():
    db = SessionLocal()
    repository = SqlAlchemyUserRepository(db)
    
    user_id = uuid.uuid4()
    test_email = f"update_{user_id}@test.com"
    test_password = "oldPassword123"
    
    new_user = User(
        id=user_id,
        email=test_email,
        full_name="Usuario Antes Update",
        hashed_password=get_password_hash(test_password),
        role=Role.TECNICO
    )
    
    repository.save(new_user)
    db.close()
    
    # 1. Hacer Login para obtener token
    response = client.post("/login", data={"username": test_email, "password": test_password})
    token = response.json()["access_token"]
    
    return {
        "email": test_email,
        "old_password": test_password,
        "id": str(user_id),
        "token": token
    }

def test_update_user_full_name(setup_update_user):
    """Test 1: Actualizar el nombre completo y verificar el cambio."""
    headers = {"Authorization": f"Bearer {setup_update_user['token']}"}
    payload = {"full_name": "Usuario Despues Update"}
    
    response = client.patch("/users/me", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Perfil actualizado correctamente"
    
    # Verificar en BBDD a través de un nuevo login (el token sigue valiendo porque no cambió el pwd)
    db = SessionLocal()
    repo = SqlAlchemyUserRepository(db)
    updated_user = repo.get_by_email(setup_update_user["email"])
    db.close()
    
    assert updated_user is not None
    assert updated_user.full_name == "Usuario Despues Update"

def test_update_user_password(setup_update_user):
    """Test 2: Actualizar la contraseña y verificar que el login funciona con la nueva."""
    headers = {"Authorization": f"Bearer {setup_update_user['token']}"}
    new_password = "newPassword456"
    payload = {"password": new_password}
    
    response = client.patch("/users/me", json=payload, headers=headers)
    assert response.status_code == 200
    
    # Intentar login con la contra vieja debe fallar
    response_old = client.post("/login", data={
        "username": setup_update_user["email"],
        "password": setup_update_user["old_password"]
    })
    assert response_old.status_code == 401
    
    # Intentar login con la contra nueva debe tener éxito
    response_new = client.post("/login", data={
        "username": setup_update_user["email"],
        "password": new_password
    })
    assert response_new.status_code == 200
    assert "access_token" in response_new.json()

def test_update_user_another_email_in_use(setup_update_user):
    """Integridad: Intentar actualizar a un email ocupado."""
    # Create conflicting user with random email to avoid persistence collisions
    db = SessionLocal()
    repo = SqlAlchemyUserRepository(db)
    uid = uuid.uuid4()
    occupied_email = f"occupied_{uid}@test.com"
    repo.save(User(
        id=uid,
        email=occupied_email,
        full_name="Occupied",
        hashed_password=get_password_hash("pwd"),
        role=Role.TECNICO
    ))
    db.close()
    
    headers = {"Authorization": f"Bearer {setup_update_user['token']}"}
    payload = {"email": occupied_email}
    
    response = client.patch("/users/me", json=payload, headers=headers)
    assert response.status_code == 400
    assert "ya está en uso" in response.json()["detail"]
