from src.infrastructure.db.database import SessionLocal, Base, engine
from src.infrastructure.db.user_repository import SqlAlchemyUserRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.user_entities import User, Role
import uuid

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        repo = SqlAlchemyUserRepository(db)
        existing = repo.get_by_email("admin@example.com")
        if not existing:
            print("Creando usuario administrador por defecto...")
            new_user = User(
                id=uuid.uuid4(),
                email="admin@example.com",
                full_name="Administrador del Sistema",
                hashed_password=get_password_hash("password123"),
                role=Role.ADMIN
            )
            db.add(new_user)
            db.commit()
            print("Usuario creado con éxito: admin@example.com / password123")
        else:
            print("El usuario admin@example.com ya existe.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
