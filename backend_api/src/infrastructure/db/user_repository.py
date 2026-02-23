import uuid
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.user_entities import User, Role
from src.domain.user_repository_interface import UserRepository
from src.infrastructure.db.models import UserModel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: UserModel) -> Optional[User]:
        if not model:
            return None
        return User(
            id=model.id,
            email=model.email,
            full_name=model.nombre,
            hashed_password=model.password_hash,
            role=model.rol
        )

    def save(self, user: User) -> None:
        user_model = UserModel(
            id=user.id,
            email=user.email,
            nombre=user.full_name,
            password_hash=user.hashed_password,
            rol=user.role
        )
        self.session.add(user_model)
        self.session.commit()

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(model)

    def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        model = self.session.query(UserModel).filter(UserModel.id == id).first()
        return self._to_domain(model)
