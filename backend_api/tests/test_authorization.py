import pytest
import uuid
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.db.sqlalchemy_repository import SqlAlchemyInspeccionRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.user_entities import User, Role
from src.domain.entities import Inspeccion, CoordenadasUTM
from datetime import date

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_setup():
    db = SessionLocal()
    user_repo = SqlAlchemyUserRepository(db)
    insp_repo = SqlAlchemyInspeccionRepository(db)
    
    # 1. Crear Tecnico 1
    t1_id = uuid.uuid4()
    t1_email = f"tecnico1_{t1_id}@test.com"
    t1 = User(id=t1_id, email=t1_email, full_name="Tecnico 1", hashed_password=get_password_hash("pwd"), role=Role.TECNICO)
    user_repo.save(t1)
    
    # 2. Crear Tecnico 2
    t2_id = uuid.uuid4()
    t2_email = f"tecnico2_{t2_id}@test.com"
    t2 = User(id=t2_id, email=t2_email, full_name="Tecnico 2", hashed_password=get_password_hash("pwd"), role=Role.TECNICO)
    user_repo.save(t2)
    
    # 3. Crear Supervisor
    sup_id = uuid.uuid4()
    sup_email = f"sup_{sup_id}@test.com"
    sup = User(id=sup_id, email=sup_email, full_name="Supervisor", hashed_password=get_password_hash("pwd"), role=Role.SUPERVISOR)
    user_repo.save(sup)
    
    # 4. Crear Inspeccion asociada a Tecnico 1
    insp_id = uuid.uuid4()
    insp_pozo = f"P-TEST-{uuid.uuid4().hex[:6]}"
    insp = Inspeccion(
        id=insp_id, id_pozo=insp_pozo, coordenadas_utm=CoordenadasUTM(x=100.0, y=100.0),
        tecnico_id=t1_id, fecha_inspec=date.today(), calle_zona="Z", situacion="Acera",
        cota_tapa=1.0, profundidad_m=1.0, estado="BUENO", material_pozo="HORMIGON",
        tipo_acceso="LIBRE", num_pates=0, forma_pozo="CIRCULAR", diametro_pozo_mm=1000,
        tapa_forma="CIRCULAR", tapa_tipo="ABISAGRADA", tapa_material="FUNDICION", 
        tapa_diametro_mm=600, red_tipo="SANEAMIENTO", colector_mat_entrada="PVC",
        colector_diametro_entrada_mm=315, colector_mat_salida="PVC", 
        colector_diametro_salida_mm=400, acometidas=[]
    )
    insp_repo.save(insp)
    db.close()
    
    # Logins para tokens
    tokens = {}
    for email in [t1_email, t2_email, sup_email]:
        res = client.post("/login", data={"username": email, "password": "pwd"})
        tokens[email] = res.json()["access_token"]
        
    return {
        "t1_token": tokens[t1_email],
        "t2_token": tokens[t2_email],
        "sup_token": tokens[sup_email],
        "insp_id": str(insp_id)
    }

def test_tecnico_cannot_edit_others_inspeccion(auth_setup):
    """Test 1: Un TÉCNICO intenta editar un pozo que NO es suyo -> 403."""
    headers = {"Authorization": f"Bearer {auth_setup['t2_token']}"}  # Tecnico 2 token
    payload = {"estado": "MALO"}
    res = client.patch(f"/inspecciones/{auth_setup['insp_id']}", json=payload, headers=headers)
    assert res.status_code == 403
    assert "No tienes permisos" in res.json()["detail"]

def test_tecnico_can_edit_own_inspeccion(auth_setup):
    """Test 2: Un TÉCNICO edita SU propio pozo -> 200/204."""
    headers = {"Authorization": f"Bearer {auth_setup['t1_token']}"}  # Tecnico 1 token (owner)
    payload = {"estado": "REGULAR"}
    res = client.patch(f"/inspecciones/{auth_setup['insp_id']}", json=payload, headers=headers)
    assert res.status_code == 200

def test_supervisor_can_edit_any_inspeccion(auth_setup):
    """Test 3: Un SUPERVISOR edita cualquier pozo -> 200."""
    headers = {"Authorization": f"Bearer {auth_setup['sup_token']}"}  # Supervisor token
    payload = {"estado": "MALO"}
    res = client.patch(f"/inspecciones/{auth_setup['insp_id']}", json=payload, headers=headers)
    assert res.status_code == 200

def test_tecnico_cannot_create_user(auth_setup):
    """Test 4: Un TÉCNICO intenta crear otro usuario -> 403."""
    headers = {"Authorization": f"Bearer {auth_setup['t1_token']}"}
    payload = {
        "email": "hacked@test.com",
        "full_name": "Hacker",
        "password": "securepwd",
        "role": "TECNICO"
    }
    res = client.post("/users", json=payload, headers=headers)
    assert res.status_code == 403
    assert "Solo los administradores" in res.json()["detail"]
