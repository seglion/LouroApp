import uuid
from src.domain.user_entities import User, Role
from src.infrastructure.db.database import SessionLocal
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository

def test_user_repository_save_and_retrieve():
    db = SessionLocal()
    repository = SqlAlchemyUserRepository(db)
    
    # 1. Crear Entidad User
    user_id = uuid.uuid4()
    test_email = f"tecnico_{user_id}@test.com"
    
    new_user = User(
        id=user_id,
        email=test_email,
        full_name="Técnico de Pruebas",
        hashed_password="hashed_dummy_password",
        role=Role.TECNICO
    )
    
    # 2. Guardar en Base de Datos
    repository.save(new_user)
    
    # 3. Recuperar y verificar
    retrieved_user = repository.get_by_email(test_email)
    
    assert retrieved_user is not None
    assert retrieved_user.id == user_id
    assert retrieved_user.email == test_email
    assert retrieved_user.full_name == "Técnico de Pruebas"
    assert retrieved_user.role == Role.TECNICO
    
    db.close()
