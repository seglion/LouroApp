import uuid
from src.domain.user_entities import User, Role
from src.domain.user_repository_interface import UserRepository
from src.domain.policies import can_create_user, ForbiddenError
from src.infrastructure.security.hashing import get_password_hash

class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, current_user: User, email: str, full_name: str, password: str, role: Role) -> User:
        if not can_create_user(current_user):
            raise ForbiddenError("Solo los administradores pueden crear nuevos usuarios.")
            
        existing = self.repository.get_by_email(email)
        if existing:
            raise ValueError(f"El email {email} ya se encuentra registrado.")
            
        new_user = User(
            id=uuid.uuid4(),
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=role
        )
        self.repository.save(new_user)
        return new_user
