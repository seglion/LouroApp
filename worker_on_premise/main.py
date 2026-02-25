import os
import sys
import shutil
import pika
import time
import json
import logging
import sqlite3
import fiona
from typing import Optional

import boto3
from botocore.exceptions import ClientError

import geopandas as gpd
from shapely.geometry import Point, mapping

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
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'gis-saneamiento-minio:9000').strip()
MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER', os.getenv('MINIO_ACCESS_KEY', 'minioadmin')).strip()
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD', os.getenv('MINIO_SECRET_KEY', 'minioadmin')).strip()
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'gis-captures').strip()
MINIO_SECURE = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
APP_DATA_DIR = os.getenv('APP_DATA_DIR', '/app/data')
DB_DIR = os.getenv('DB_DIR', '/app/db')  # Nueva carpeta para evitar bloqueos en red (CIFS)
DB_PATH = os.path.join(DB_DIR, 'idempotency.db')
HOST_DATA_PATH = os.getenv('HOST_DATA_PATH', 'X:') # Ruta base en el Host (Windows/Samba)

def translate_to_host_path(local_path: str) -> str:
    """Traduce una ruta interna /app/data/... a una ruta de Windows X:\..."""
    if not local_path:
        return ""
    # Normalizamos el separador a Windows si el Host base parece ser Windows
    path = local_path.replace(APP_DATA_DIR, HOST_DATA_PATH)
    if "\\" in HOST_DATA_PATH or ":" in HOST_DATA_PATH or HOST_DATA_PATH.startswith("//"):
        path = path.replace("/", "\\")
        # Corregir dobles barras si ocurren por el replace inicial, excepto al inicio de UNC
        if not path.startswith("\\\\"):
            path = path.replace("\\\\", "\\")
    return path

EXCHANGE_NAME = 'inspecciones.v1'
QUEUE_NAME = 'worker_on_premise_queue'
ROUTING_KEY = 'inspeccion.*'

# ---------------------------------------------------------
# Idempotencia: Base de datos SQLite local
# ---------------------------------------------------------
def init_db():
    """
    Inicializa la base de datos local SQLite para control de idempotencia en un storage fiable.
    """
    os.makedirs(DB_DIR, exist_ok=True)
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
def process_message(ch, method, properties, body):
    """
    Callback principal para manejar mensajes entrantes de RabbitMQ.
    Aseguramos ACK manual para evitar pérdida temporal de mensajes.
    """
    try:
        message = json.loads(body)
        metadata = message.get("metadata", {})
        event_id = metadata.get("event_id")
        event_type = metadata.get("event_type")

        if not event_id:
            logger.error(f"Mensaje malformado: no contiene 'event_id'. Body: {body}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info(f"📝 Recibido evento [{event_id}] (Tipo: {event_type})")

        # 1. VERIFICACIÓN DE IDEMPOTENCIA
        if is_event_processed(event_id):
            logger.warning(f"⏩ Evento [{event_id}] ignorado. Ya fue procesado exitosamente en el Worker On-Premise.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # 2. PROCESO DE INTEGRACIÓN
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
            config=boto3.session.Config(signature_version='s3v4'),
            region_name='us-east-1'
        )

        urls_a_descargar = []
        # Si la API envía 'foto_keys', las usamos. Si no, probamos con los campos antiguos (retrocompatibilidad)
        foto_keys = pozo.get("foto_keys", [])
        for key in foto_keys:
            # Si el key ya es una URI completa s3://... la usamos, si no, la construimos.
            if key.startswith("s3://"):
                urls_a_descargar.append(key)
            else:
                urls_a_descargar.append(f"s3://{MINIO_BUCKET}/{key}")

        # Retrocompatibilidad con campos específicos si no hay foto_keys
        if not urls_a_descargar:
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

        # --------------------------------------------------
        # HITO 4: GENERACIÓN Y ACTUALIZACIÓN DE CAPAS (GeoPackage)
        # --------------------------------------------------
        # ESTRATEGIA: Para evitar "database is locked" en CIFS, trabajamos en LOCAL y luego subimos.
        remote_gpkg_path = os.path.join(APP_DATA_DIR, "Inspecciones_Recientes.gpkg")
        local_gpkg_path = os.path.join(DB_DIR, "Inspecciones_Recientes_Buffer.gpkg")
        
        coord = pozo.get("coordenadas_utm", {})
        x_val = coord.get("x")
        y_val = coord.get("y")
        epsg = coord.get("epsg", 25829)

        if x_val is not None and y_val is not None:
            geom = Point(x_val, y_val)
            
            def clean_val(key, default=None):
                v = pozo.get(key)
                return v if v is not None else default

            # Lógica inteligente para asignar fotos a campos específicos
            foto_keys = pozo.get("foto_keys", [])
            path_situacion = ""
            path_interior = ""
            
            for key in foto_keys:
                filename = key.split("/")[-1]
                full_local_path = os.path.join(download_dir, filename)
                if "_situacion" in filename.lower():
                    path_situacion = full_local_path
                elif "_interior" in filename.lower() or "_pozo" in filename.lower():
                    path_interior = full_local_path
            
            # Fallback a campos antiguos por si acaso
            if not path_situacion and pozo.get("ruta_foto_situacion"):
                path_situacion = os.path.join(download_dir, pozo.get("ruta_foto_situacion", "").split("/")[-1])
            if not path_interior and pozo.get("ruta_foto_interior"):
                path_interior = os.path.join(download_dir, pozo.get("ruta_foto_interior", "").split("/")[-1])

            row_data = {
                "id": clean_val("id", ""),
                "id_pozo": clean_val("id_pozo", "N/A"),
                "fecha_inspec": clean_val("fecha_inspec", ""),
                "calle_zona": clean_val("calle_zona", ""),
                "situacion": clean_val("situacion", ""),
                "cota_tapa": float(pozo.get("cota_tapa") or 0.0),
                "profundidad_m": float(pozo.get("profundidad_m") or 0.0),
                "estado": clean_val("estado", ""),
                "material_pozo": clean_val("material_pozo", ""),
                "tipo_acceso": clean_val("tipo_acceso", ""),
                "num_pates": int(pozo.get("num_pates") or 0),
                "forma_pozo": clean_val("forma_pozo", ""),
                "diametro_pozo_mm": int(pozo.get("diametro_pozo_mm") or 0),
                "largo_pozo_mm": int(pozo.get("largo_pozo_mm") or 0),
                "ancho_pozo_mm": int(pozo.get("ancho_pozo_mm") or 0),
                "resalto": clean_val("resalto", ""),
                "filtraciones": clean_val("filtraciones", ""),
                "pluviales": clean_val("pluviales", ""),
                "biofilm": clean_val("biofilm", ""),
                "tapa_forma": clean_val("tapa_forma", ""),
                "tapa_tipo": clean_val("tapa_tipo", ""),
                "tapa_material": clean_val("tapa_material", ""),
                "tapa_diametro_mm": int(pozo.get("tapa_diametro_mm") or 0),
                "tapa_largo_mm": int(pozo.get("tapa_largo_mm") or 0),
                "tapa_ancho_mm": int(pozo.get("tapa_ancho_mm") or 0),
                "red_tipo": clean_val("red_tipo", ""),
                "red_viene_de_pozo": clean_val("red_viene_de_pozo", ""),
                "red_va_a_pozo": clean_val("red_va_a_pozo", ""),
                "red_carga": clean_val("red_carga", ""),
                "colector_mat_entrada": clean_val("colector_mat_entrada", ""),
                "colector_diametro_entrada_mm": int(pozo.get("colector_diametro_entrada_mm") or 0),
                "colector_mat_salida": clean_val("colector_mat_salida", ""),
                "colector_diametro_salida_mm": int(pozo.get("colector_diametro_salida_mm") or 0),
                "ruta_foto_situacion": translate_to_host_path(path_situacion),
                "ruta_foto_interior": translate_to_host_path(path_interior),
                "observaciones": clean_val("observaciones", ""),
                "geometry": geom
            }

            acometidas = payload.get("acometidas", [])
            row_data["num_acometidas"] = len(acometidas)
            row_data["acometidas_json"] = json.dumps(acometidas) if acometidas else ""

            schema = {
                "geometry": "Point",
                "properties": {
                    "id": "str", "id_pozo": "str", "fecha_inspec": "str", "calle_zona": "str",
                    "situacion": "str", "cota_tapa": "float", "profundidad_m": "float",
                    "estado": "str", "material_pozo": "str", "tipo_acceso": "str",
                    "num_pates": "int", "forma_pozo": "str", "diametro_pozo_mm": "int",
                    "largo_pozo_mm": "int", "ancho_pozo_mm": "int", "resalto": "str",
                    "filtraciones": "str", "pluviales": "str", "biofilm": "str",
                    "tapa_forma": "str", "tapa_tipo": "str", "tapa_material": "str",
                    "tapa_diametro_mm": "int", "tapa_largo_mm": "int", "tapa_ancho_mm": "int",
                    "red_tipo": "str", "red_viene_de_pozo": "str", "red_va_a_pozo": "str",
                    "red_carga": "str", "colector_mat_entrada": "str", "colector_diametro_entrada_mm": "int",
                    "colector_mat_salida": "str", "colector_diametro_salida_mm": "int",
                    "ruta_foto_situacion": "str", "ruta_foto_interior": "str",
                    "observaciones": "str", "num_acometidas": "int", "acometidas_json": "str"
                }
            }

            if os.path.exists(remote_gpkg_path) and os.path.getsize(remote_gpkg_path) > 0:
                shutil.copy2(remote_gpkg_path, local_gpkg_path)
            
            # LÓGICA DE UPSERT: Si existe, lo borramos y escribimos el nuevo
            existing_features = []
            if os.path.exists(local_gpkg_path):
                try:
                    with fiona.open(local_gpkg_path, "r") as source:
                        # Guardamos todos los que NO coincidan con nuestro ID
                        for feature in source:
                            if feature["properties"].get("id") != row_data["id"]:
                                existing_features.append(feature)
                except Exception as e:
                    logger.warning(f"No se pudo leer GPKG existente para Upsert: {e}")

            logger.info(f"🗺️  Actualizando buffer GIS local (Upsert)...")
            # Escribimos de nuevo (modo 'w' para sobreescribir con la lista filtrada + el nuevo)
            with fiona.open(local_gpkg_path, "w", driver="GPKG", schema=schema, crs=f"EPSG:{epsg}", layer="pozos_inspeccionados") as layer:
                # Escribimos los existentes preservados
                for feat in existing_features:
                    layer.write(feat)
                # Escribimos el nuevo/actualizado
                props = {k: v for k, v in row_data.items() if k != "geometry"}
                layer.write({"geometry": mapping(geom), "properties": props})

            logger.info(f"📤 Sincronizando GeoPackage con unidad de red: {remote_gpkg_path}")
            shutil.copy2(local_gpkg_path, remote_gpkg_path)
        else:
            logger.warning("No se incluyeron coordenadas espaciales válidas. Omitiendo volcado a GIS.")

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
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)

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
