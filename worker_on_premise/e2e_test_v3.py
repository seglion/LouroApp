import os
import time
import json
import boto3
import pika

# Load Env Vars
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS_KEY = 'admin_minio'
MINIO_SECRET_KEY = 'minio_dev_pass'

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin_rabbit'
RABBITMQ_PASS = 'rabbit_dev_pass'

# Setup MinIO
print("Connecting to MinIO to setup buckets and files...")
s3 = boto3.client('s3',
                  endpoint_url=f"http://{MINIO_ENDPOINT}",
                  aws_access_key_id=MINIO_ACCESS_KEY,
                  aws_secret_access_key=MINIO_SECRET_KEY,
                  region_name='us-east-1')

bucket_name = "gis-captures"
try:
    s3.create_bucket(Bucket=bucket_name)
except Exception as e:
    print(f"Bucket probably exists: {e}")

# Upload Mock Photos
mock_photos = [
    "2026/02/P-9000/situacion.jpg",
    "2026/02/P-9000/interior.jpg"
]
for photo in mock_photos:
    s3.put_object(Bucket=bucket_name, Key=photo, Body=b"fake-image-content")
print("Mock files uploaded to MinIO.")

# Publish RabbitMQ Message
print(f"Connecting to RabbitMQ to publish message... {RABBITMQ_HOST}:{RABBITMQ_PORT}")
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
channel = connection.channel()

exchange_name = 'gis_events_exchange'
queue_name = 'worker_on_premise_queue'
routing_key = 'inspeccion.creada'

channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='inspeccion.*')

event_id = f"e2e-final-{int(time.time())}"
payload = {
    "metadata": {
        "event_id": event_id,
        "event_type": "inspeccion.creada",
        "timestamp": "2026-02-25T13:30:00Z"
    },
    "payload": {
        "pozo": {
            "id": event_id,
            "id_pozo": "P-VOLUMEN-X",
            "fecha_inspec": "2026-02-25",
            "calle_zona": "Calle del Volumen Externo",
            "coordenadas_utm": {"x": 537000, "y": 4680000, "epsg": 25829},
            "ruta_foto_situacion": f"s3://{bucket_name}/{mock_photos[0]}",
            "ruta_foto_interior": f"s3://{bucket_name}/{mock_photos[1]}"
        }
    }
}

channel.basic_publish(
    exchange=exchange_name,
    routing_key=routing_key,
    body=json.dumps(payload),
    properties=pika.BasicProperties(delivery_mode=2)
)

print(f"Mock event [{event_id}] published to RabbitMQ.")
connection.close()
