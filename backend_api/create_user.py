"""
Script para crear usuarios en la base de datos.
Ejecutar dentro del contenedor Docker:
  docker exec -it gis_saneamiento_api python create_user.py
"""
import sys
import os
import uuid
sys.path.insert(0, '/app')

from src.infrastructure.db.database import SessionLocal, Base, engine
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.user_entities import User, Role

def create_user(email: str, full_name: str, password: str, role: str = "TECNICO"):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        repo = SqlAlchemyUserRepository(db)
        existing = repo.get_by_email(email)
        if existing:
            print(f"❌ El usuario '{email}' ya existe.")
            return

        role_enum = Role[role.upper()]
        new_user = User(
            id=uuid.uuid4(),
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=role_enum
        )
        repo.save(new_user)
        db.commit()
        print(f"✅ Usuario creado: {email} (rol: {role_enum.value})")
    except KeyError:
        print(f"❌ Rol inválido: '{role}'. Usa: TECNICO o ADMIN")
    finally:
        db.close()

if __name__ == "__main__":
    # Valores por defecto si no se pasan argumentos
    email     = sys.argv[1] if len(sys.argv) > 1 else "admin@aquatica.com"
    full_name = sys.argv[2] if len(sys.argv) > 2 else "Administrador Aquatica"
    password  = sys.argv[3] if len(sys.argv) > 3 else "password123"
    role      = sys.argv[4] if len(sys.argv) > 4 else "ADMIN"

    create_user(email, full_name, password, role)
