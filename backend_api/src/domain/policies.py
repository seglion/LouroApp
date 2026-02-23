from src.domain.user_entities import User, Role
from src.domain.entities import Inspeccion

class ForbiddenError(Exception):
    pass

def can_create_inspeccion(user: User) -> bool:
    # Cualquier usuario autenticado puede crear
    return user is not None

def can_edit_inspeccion(user: User, inspeccion: Inspeccion) -> bool:
    if user.role in [Role.ADMIN, Role.SUPERVISOR]:
        return True
    if user.id == inspeccion.tecnico_id:
        return True
    return False

def can_create_user(user: User) -> bool:
    return user.role == Role.ADMIN

def can_edit_user(user: User, target_user: User) -> bool:
    if user.role == Role.ADMIN:
        return True
    if user.id == target_user.id:
        return True
    return False
