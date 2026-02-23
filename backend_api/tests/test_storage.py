import pytest
import uuid
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.infrastructure.api.main import app, get_current_user, get_minio_client
from src.domain.user_entities import User, Role
from src.domain.entities import Inspeccion, CoordenadasUTM
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.sqlalchemy_repository import SqlAlchemyInspeccionRepository
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository

client = TestClient(app)

mock_minio = MagicMock()
current_test_user = None

def mock_get_current_user():
    return current_test_user

@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_minio_client] = lambda: mock_minio
    yield
    mock_minio.reset_mock()
    app.dependency_overrides.clear()

@pytest.fixture
def auth_setup():
    db = SessionLocal()
    user_repo = SqlAlchemyUserRepository(db)
    
    owner = User(id=uuid.uuid4(), email=f"owner_{uuid.uuid4().hex[:6]}@test.com", full_name="O", hashed_password="x", role=Role.TECNICO)
    other = User(id=uuid.uuid4(), email=f"other_{uuid.uuid4().hex[:6]}@test.com", full_name="O", hashed_password="x", role=Role.TECNICO)
    user_repo.save(owner)
    user_repo.save(other)
    
    insp_id = uuid.uuid4()
    pozo = Inspeccion(
        id=insp_id, id_pozo=f"P-{uuid.uuid4().hex[:6]}",
        coordenadas_utm=CoordenadasUTM(x=0, y=0), tecnico_id=owner.id
    )
    repo = SqlAlchemyInspeccionRepository(db)
    repo.save(pozo)
    db.close()
    
    return {"owner": owner, "other": other, "insp_id": insp_id}    

def test_upload_photo_success_owner(auth_setup):
    global current_test_user
    current_test_user = auth_setup["owner"]
    mock_minio.upload_file.return_value = "P-STORAGE/fake.jpg"

    file_payload = {"file": ("test.jpg", b"fake byte data", "image/jpeg")}
    response = client.post(f"/inspecciones/{auth_setup['insp_id']}/photos", files=file_payload)
    
    assert response.status_code == 201
    assert "status" in response.json()
    assert response.json()["status"] == "success"
    assert "P-STORAGE/fake.jpg" in response.json()["foto_keys"]
    
    mock_minio.upload_file.assert_called_once()
    
def test_upload_photo_forbidden_other_tecnico(auth_setup):
    global current_test_user
    current_test_user = auth_setup["other"]

    file_payload = {"file": ("test.jpg", b"fake byte data", "image/jpeg")}
    response = client.post(f"/inspecciones/{auth_setup['insp_id']}/photos", files=file_payload)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "No tienes permisos para añadir fotos a esta inspección."
    mock_minio.upload_file.assert_not_called()
