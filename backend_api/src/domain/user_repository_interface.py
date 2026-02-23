import uuid
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.user_entities import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass
