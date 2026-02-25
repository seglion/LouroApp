import pika
import json
import logging
import os
from src.domain.events import InspeccionCreadaEvent
from src.domain.event_publisher_interface import EventPublisher

logger = logging.getLogger(__name__)

class RabbitMQPublisher(EventPublisher):
    def __init__(self, host: str = "gis_saneamiento_rabbit", exchange: str = "inspecciones.v1"):
        self.host = host
        self.exchange = exchange
        self.user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
        self.password = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
        
    def _create_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, 
            credentials=credentials,
            heartbeat=60
        )
        return pika.BlockingConnection(parameters)

    def publish(self, event: any) -> None:
        try:
            from dataclasses import asdict
            from datetime import datetime
            import uuid
            
            def custom_serializer(obj):
                if isinstance(obj, uuid.UUID):
                    return str(obj)
                if hasattr(obj, 'isoformat'):
                    return obj.isoformat()
                raise TypeError(f"Type {type(obj)} not serializable")

            connection = self._create_connection()
            channel = connection.channel()
            
            channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=True)
            
            # Determinamos el tipo de evento para el routing_key y metadata
            event_type = "inspeccion.creada"
            routing_key = "inspeccion.creada"
            
            if hasattr(event, "__class__"):
                class_name = event.__class__.__name__
                if "Actualizada" in class_name:
                    event_type = "inspeccion.actualizada"
                    routing_key = "inspeccion.actualizada"
            
            # Estructura que espera el worker con idempotencia
            # Usamos un UUID nuevo para CADA publicación, así el worker no lo ignora
            message = {
                "metadata": {
                    "event_id": str(uuid.uuid4()),
                    "event_type": event_type,
                    "timestamp": datetime.utcnow().isoformat()
                },
                "payload": {
                    "pozo": asdict(event.inspeccion)
                }
            }
            
            body = json.dumps(message, default=custom_serializer)
            
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
            
            connection.close()
            logger.info(f"Published {event_type} event correctly to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to publish event to RabbitMQ: {e}")
            raise e
