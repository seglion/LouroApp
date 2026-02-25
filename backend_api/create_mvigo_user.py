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
        email = "mvigo@aquaticaingenieria.com"
        existing = repo.get_by_email(email)
        if not existing:
            print(f"Creando usuario {email}...")
            new_user = User(
                id=uuid.uuid4(),
                email=email,
                full_name="Miguel Angel Vigo Baz",
                hashed_password=get_password_hash("Aq0010cA"),
                role=Role.ADMIN
            )
            repo.save(new_user)
            print(f"Usuario creado con éxito: {email}")
        else:
            print(f"El usuario {email} ya existe.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
