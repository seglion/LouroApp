from src.domain.entities import Inspeccion
from src.domain.repository_interface import InspeccionRepository

class UpdateInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository):
        self.repository = repository

    def execute(self, inspeccion: Inspeccion) -> Inspeccion:
        existing = self.repository.get_by_id(inspeccion.id)
        if not existing:
            raise ValueError("La inspección especificada no existe.")
        
        # Regla de negocio: no editar validada
        if existing.estado == "VALIDADA":
            raise ValueError("No se puede editar una inspección que ya haya sido validada por un supervisor")
        
        self.repository.update(inspeccion)
        return inspeccion
