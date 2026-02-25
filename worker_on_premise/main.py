import os
import sys
import pika
import time
import json
import logging
import sqlite3
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# Configuración básica de observabilidad (Logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuración a través de Entorno (RabbitMQ)
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')

# Configuración a través de Entorno (MinIO)
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'gis-captures')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
APP_DATA_DIR = os.getenv('APP_DATA_DIR', '/app/data')
EXCHANGE_NAME = 'gis_events_exchange'
QUEUE_NAME = 'worker_on_premise_queue'
ROUTING_KEY = 'inspeccion.*'

# ---------------------------------------------------------
# Idempotencia: Base de datos SQLite local
# ---------------------------------------------------------
DB_PATH = os.path.join(APP_DATA_DIR, 'idempotency.db')

def init_db():
    """Crea la tabla de eventos procesados si no existe."""
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_events (
            event_id TEXT PRIMARY KEY,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    logger.info(f"Base de datos de idempotencia inicializada en: {DB_PATH}")

def is_event_processed(event_id: str) -> bool:
    """Verifica si un evento ya fue procesado mediante clave primaria."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM processed_events WHERE event_id = ?", (event_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_event_processed(event_id: str):
    """Marca un evento como completado tras una ingesta GIS exitosa."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO processed_events (event_id) VALUES (?)", (event_id,))
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# Lógica de Consumo GIS
# ---------------------------------------------------------
def process_gis_message(ch, method, properties, body):
    """
    Callback principal para manejar mensajes entrantes de RabbitMQ.
    Aseguramos ACK manual para evitar pérdida temporal de mensajes.
    """
    try:
        message = json.loads(body)
        event_id = message.get("event_id")
        
        if not event_id:
            logger.error("Mensaje malformado: no contiene 'event_id'. Descartando.")
            # Hacemos ACK porque el mensaje está roto y no queremos que se encole infinitamente.
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info(f"📝 Recibido evento [{event_id}] (Tipo: {message.get('event_type')})")

        # 1. VERIFICACIÓN DE IDEMPOTENCIA
        if is_event_processed(event_id):
            logger.warning(f"⏩ Evento [{event_id}] ignorado. Ya fue procesado exitosamente en el Worker On-Premise.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # 2. PROCESO DE INTEGRACIÓN (Hitos 3 y 4 se engancharán aquí)
        payload = message.get("payload", {})
        pozo = payload.get("pozo", {})
        id_pozo = pozo.get("id_pozo", "POZO_DESCONOCIDO")
        # Extraemos fecha de inspección (ej. "2026-02-23")
        fecha_str = pozo.get("fecha_inspec", "1970-01-01")
        try:
            anio, mes, _ = fecha_str.split('-')
        except ValueError:
            anio, mes = "XXXX", "XX"

        logger.info(f"⏳ Procesando inspección del pozo: {id_pozo}")
        
        # --------------------------------------------------
        # HITO 3: DESCARGA ASÍNCRONA DESDE MINIO
        # --------------------------------------------------
        # Estructura requerida: Descargas_GIS/{Anio}/{Mes}/{Id_Pozo}/
        download_dir = os.path.join(APP_DATA_DIR, "Descargas_GIS", anio, mes, id_pozo)
        os.makedirs(download_dir, exist_ok=True)

        s3_client = boto3.client(
            's3',
            endpoint_url=f"http{'s' if MINIO_SECURE else ''}://{MINIO_ENDPOINT}",
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name='us-east-1' # Default for MinIO compat
        )

        urls_a_descargar = []
        if pozo.get("ruta_foto_situacion"):
            urls_a_descargar.append(pozo["ruta_foto_situacion"])
        if pozo.get("ruta_foto_interior"):
            urls_a_descargar.append(pozo["ruta_foto_interior"])

        for uri in urls_a_descargar:
            # Ejemplo URI esperado: "s3://gis-captures/pozos/018e6ec2..._situacion.jpg"
            if uri.startswith("s3://"):
                # Parsear "s3://bucket/path/to/file.jpg" a "path/to/file.jpg"
                parts = uri.replace("s3://", "").split("/")
                bucket_name = parts[0]
                object_key = "/".join(parts[1:])
                filename = parts[-1]
                local_path = os.path.join(download_dir, filename)

                if not os.path.exists(local_path):
                    logger.info(f"⬇️ Descargando {filename} desde {bucket_name}/{object_key}...")
                    try:
                        s3_client.download_file(bucket_name, object_key, local_path)
                    except ClientError as e:
                        logger.error(f"Error descargando {filename} de MinIO: {e}")
                        # Propagamos excepcion para no hacer ACK y reintentar si es necesario.
                        raise
                else:
                    logger.info(f"🆗 Archivo {filename} ya existe localmente. Omitiendo.")
            else:
                logger.warning(f"URI de imagen no reconocida: {uri}")

        # 3. ÉXITO: MARCAR PROCESADO Y NOTIFICAR AL BROKER (ACK)
        mark_event_processed(event_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"✅ Evento [{event_id}] completado y Ack enviado a RabbitMQ.")

    except json.JSONDecodeError:
        logger.error(f"Error parseando JSON: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        # En un fallo en tiempo de ejecución (falla MinIO o escritura GPKG), NO HACEMOS ACK
        # El mensaje viaja de nuevo a RabbitMQ para reintentarse (At-Least-Once Delivery).
        logger.error(f"❌ Error catastrófico procesando mensaje [{event_id}]: {str(e)}")
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) 
        # Cuidado con los bucles infinitos en errores lógicos, en Producción se mandarían a una DLQ.
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

# ---------------------------------------------------------
# Ciclo de Vida y Resiliencia (Reconexión de RabbitMQ)
# ---------------------------------------------------------
def consume():
    """
    Se conecta robustamente a RabbitMQ. Si falla, espera y reintenta
    de forma infinita. Esto tolera reinicios o desconexiones del Cloud.
    """
    init_db()
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=60,                # Tolerancia a cortes de red PWA/3G/VPN
        blocked_connection_timeout=300
    )

    while True:
        try:
            logger.info(f"Intentando conectar a RabbitMQ en {RABBITMQ_HOST}:{RABBITMQ_PORT}...")
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declaramos la topología (Por si el RabbitMQ se acaba de crear y está vacío)
            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

            # Para consumo justo: el worker recibe 1 mensaje máximo antes de mandar el ACK
            channel.basic_qos(prefetch_count=1)

            # Consumo manual
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_gis_message)

            logger.info(f"🎧 GIS Worker On-Premise escuchando eventos en la cola '{QUEUE_NAME}'...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Conexión perdida o rechazada por RabbitMQ: {e}.")
            logger.info("Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Worker detenido manualmente (Ctrl+C). Cierre limpio.")
            if 'connection' in locals() and connection.is_open:
                connection.close()
            sys.exit(0)
        except Exception as e:
            logger.error(f"Fallo no contemplado en bucle principal: {e}")
            logger.info("Reintentando en 10 segundos para no saturar...")
            time.sleep(10)

if __name__ == "__main__":
    consume()
