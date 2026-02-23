from src.domain.entities import Inspeccion
from src.domain.user_entities import User
from src.domain.policies import can_edit_inspeccion, ForbiddenError
from src.domain.repository_interface import InspeccionRepository

class UpdateInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository):
        self.repository = repository

    def execute(self, inspeccion: Inspeccion, current_user: User) -> Inspeccion:
        existing = self.repository.get_by_id(inspeccion.id)
        if not existing:
            raise ValueError("La inspección especificada no existe.")
            
        if not can_edit_inspeccion(current_user, existing):
            raise ForbiddenError("No tienes permisos para editar esta inspección.")
        
        # Regla de negocio: no editar validada
        if existing.estado == "VALIDADA":
            raise ValueError("No se puede editar una inspección que ya haya sido validada por un supervisor")
        
        self.repository.update(inspeccion)
        return inspeccion
