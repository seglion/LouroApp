import uuid
from dataclasses import dataclass
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    TECNICO = "TECNICO"

@dataclass
class User:
    id: uuid.UUID
    email: str
    full_name: str
    hashed_password: str
    role: Role
