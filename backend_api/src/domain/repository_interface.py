import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities import Inspeccion

class InspeccionRepository(ABC):
    @abstractmethod
    def save(self, inspeccion: Inspeccion) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Optional[Inspeccion]:
        pass

    @abstractmethod
    def get_by_pozo_code(self, code: str) -> Optional[Inspeccion]:
        pass

    @abstractmethod
    def update(self, inspeccion: Inspeccion) -> None:
        pass
