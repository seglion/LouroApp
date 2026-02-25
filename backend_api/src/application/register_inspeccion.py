import uuid
import logging
from typing import Optional
from src.domain.entities import Inspeccion
from src.domain.repository_interface import InspeccionRepository
from src.domain.user_repository_interface import UserRepository
from src.domain.event_publisher_interface import EventPublisher
from src.domain.events import InspeccionCreadaEvent
from datetime import datetime

logger = logging.getLogger(__name__)

class RegisterInspeccionUseCase:
    def __init__(self, repository: InspeccionRepository, 
                 user_repo: Optional[UserRepository] = None,
                 event_publisher: Optional[EventPublisher] = None):
        self.repository = repository
        self.user_repo = user_repo
        self.event_publisher = event_publisher

    def execute(self, inspeccion: Inspeccion) -> Inspeccion:
        if not inspeccion.id or not inspeccion.id_pozo:
            raise ValueError("ID e ID de Pozo son obligatorios")
            
        if inspeccion.tecnico_id and self.user_repo:
             # Opcional validar que el tecnico exista
             user = self.user_repo.get_by_id(inspeccion.tecnico_id)
             if not user:
                 raise ValueError("El técnico asignado no existe.")
        
        self.repository.save(inspeccion)
        
        # Publicar el evento de dominio de forma segura
        if self.event_publisher:
            try:
                evento = InspeccionCreadaEvent(
                    id_inspeccion=inspeccion.id,
                    id_pozo=inspeccion.id_pozo,
                    tecnico_id=inspeccion.tecnico_id,
                    timestamp=datetime.utcnow(),
                    inspeccion=inspeccion
                )
                self.event_publisher.publish(evento)
            except Exception as e:
                # Log the error but NEVER crash the transaction
                logger.error(f"Error publicando el evento InspeccionCreadaEvent para {inspeccion.id}: {e}")
                
        return inspeccion
