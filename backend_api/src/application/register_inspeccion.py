from src.domain.entities import Inspeccion
from src.domain.repository_interface import InspeccionRepository

class RegisterInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository):
        self.repository = repository

    def execute(self, inspeccion: Inspeccion) -> Inspeccion:
        if not inspeccion.id or not inspeccion.id_pozo:
            raise ValueError("La inspección debe tener ID y ID Pozo válidos.")
        
        self.repository.save(inspeccion)
        return inspeccion
