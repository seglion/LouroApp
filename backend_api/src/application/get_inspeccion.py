import uuid
from typing import Optional
from src.domain.entities import Inspeccion
from src.domain.repository_interface import InspeccionRepository

class GetInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository):
        self.repository = repository

    def get_by_id(self, id: uuid.UUID) -> Optional[Inspeccion]:
        return self.repository.get_by_id(id)

    def get_by_pozo_code(self, code: str) -> Optional[Inspeccion]:
        return self.repository.get_by_pozo_code(code)
