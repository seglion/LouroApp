import uuid
from datetime import datetime
from dataclasses import dataclass

@dataclass
class InspeccionCreadaEvent:
    id_inspeccion: uuid.UUID
    id_pozo: str
    tecnico_id: uuid.UUID
    timestamp: datetime
