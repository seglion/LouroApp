import uuid
from typing import BinaryIO
from src.domain.repository_interface import InspeccionRepository
from src.domain.policies import can_edit_inspeccion, ForbiddenError
from src.domain.user_entities import User
from src.infrastructure.storage.minio_client import MinioStorageClient

from src.domain.event_publisher_interface import EventPublisher
from src.domain.events import InspeccionActualizadaEvent
from datetime import datetime

class UploadInspeccionFotoUseCase:
    def __init__(self, repository: InspeccionRepository, storage: MinioStorageClient, event_publisher: EventPublisher = None):
        self.repository = repository
        self.storage = storage
        self.event_publisher = event_publisher

    def execute(self, inspeccion_id: uuid.UUID, file_data, file_name: str, content_type: str, current_user: User) -> list[str]:
        # 1. Recuperar la inspección
        inspeccion = self.repository.get_by_id(inspeccion_id)
        if not inspeccion:
            raise ValueError(f"Inspección con id {inspeccion_id} no encontrada.")

        # 2. Verificar políticas de Autorización
        if not can_edit_inspeccion(current_user, inspeccion):
            raise ForbiddenError("No tienes permisos para añadir fotos a esta inspección.")

        # 3. Construir la ruta preservando el sufijo del nombre enviado por el cliente
        # file_name típico: "{uuid}_situacion.jpg" o "{uuid}_pozo.jpg"
        # Resultado: "{id_pozo}/{uuid}_situacion.jpg"
        extension = file_name.split('.')[-1] if '.' in file_name else 'jpg'
        stem = file_name.rsplit('.', 1)[0] if '.' in file_name else file_name
        unique_file_name = f"{inspeccion.id_pozo}/{stem}.{extension}"

        # 4. Subir la imagen a MinIO
        file_key = self.storage.upload_file(
            file_data=file_data,
            file_name=unique_file_name,
            content_type=content_type
        )

        # 5. Agregar el key de la foto al array de la entidad
        if not inspeccion.foto_keys:
            inspeccion.foto_keys = []
        inspeccion.foto_keys.append(file_key)

        # 6. Guardar cambios en la Base de Datos
        self.repository.update(inspeccion)

        # 7. Notificar actualización (opcional si hay publicador)
        if self.event_publisher:
            try:
                evento = InspeccionActualizadaEvent(
                    id_inspeccion=inspeccion.id,
                    id_pozo=inspeccion.id_pozo,
                    tecnico_id=inspeccion.tecnico_id,
                    timestamp=datetime.utcnow(),
                    inspeccion=inspeccion
                )
                self.event_publisher.publish(evento)
            except Exception:
                pass # No bloqueamos la subida por fallo en mensajería

        return inspeccion.foto_keys
