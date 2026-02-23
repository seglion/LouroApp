import uuid
from typing import Optional
from src.domain.entities import Inspeccion
from src.domain.repository_interface import InspeccionRepository
from src.domain.user_repository_interface import UserRepository

class RegisterInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository, user_repo: Optional[UserRepository] = None):
        self.repository = repository
        self.user_repo = user_repo

    def execute(self, inspeccion: Inspeccion) -> Inspeccion:
        if not inspeccion.id or not inspeccion.id_pozo:
            raise ValueError("ID e ID de Pozo son obligatorios")
            
        if inspeccion.tecnico_id and self.user_repo:
             # Opcional validar que el tecnico exista
             user = self.user_repo.get_by_id(inspeccion.tecnico_id)
             if not user:
                 raise ValueError("El técnico asignado no existe.")
        
        self.repository.save(inspeccion)
        return inspeccion
