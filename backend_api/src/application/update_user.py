from typing import Optional
from src.domain.user_entities import User
from src.domain.user_repository_interface import UserRepository
from src.infrastructure.security.hashing import get_password_hash
from src.domain.policies import can_edit_user, ForbiddenError

class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, target_user: User, current_user: User,
                full_name: Optional[str] = None, 
                email: Optional[str] = None, 
                new_password: Optional[str] = None) -> User:
        
        if not can_edit_user(current_user, target_user):
            raise ForbiddenError("No tienes permisos para editar este perfil de usuario.")
        
        # Validar si cambiamos email (no nulo, diferente, y no usado por otro)
        if email and email != current_user.email:
            existing = self.repository.get_by_email(email)
            if existing:
                raise ValueError("El email ya está en uso.")
            current_user.email = email

        if full_name:
            current_user.full_name = full_name
            
        if new_password:
            # Hash y reemplazar la password
            current_user.hashed_password = get_password_hash(new_password)
            
        self.repository.update(current_user)
        return current_user
