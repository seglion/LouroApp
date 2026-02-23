from abc import ABC, abstractmethod
from src.domain.events import InspeccionCreadaEvent

class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: InspeccionCreadaEvent) -> None:
        pass
