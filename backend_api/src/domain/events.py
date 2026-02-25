from .entities import Inspeccion
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class InspeccionCreadaEvent:
    id_inspeccion: uuid.UUID
    id_pozo: str
    tecnico_id: uuid.UUID
    timestamp: datetime
    inspeccion: Inspeccion

@dataclass
class InspeccionActualizadaEvent:
    id_inspeccion: uuid.UUID
    id_pozo: str
    tecnico_id: uuid.UUID
    timestamp: datetime
    inspeccion: Inspeccion
