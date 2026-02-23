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

    def publish(self, event: InspeccionCreadaEvent) -> None:
        try:
            connection = self._create_connection()
            channel = connection.channel()
            
            # Asegurar exchange de tipo topic, durable
            channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=True)
            
            payload = {
                "id_inspeccion": str(event.id_inspeccion),
                "id_pozo": event.id_pozo,
                "tecnico_id": str(event.tecnico_id),
                "timestamp": event.timestamp.isoformat()
            }
            
            channel.basic_publish(
                exchange=self.exchange,
                routing_key="inspeccion.creada",
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistente
                    content_type='application/json'
                )
            )
            
            connection.close()
            logger.info(f"Published InspeccionCreadaEvent for {event.id_inspeccion} correctly to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to publish event to RabbitMQ: {e}")
            raise e
