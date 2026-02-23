import os
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
import logging

logger = logging.getLogger(__name__)

class MinioStorageClient:
    def __init__(self, endpoint: str = "gis_saneamiento_minio:9000", bucket_name: str = "inspecciones"):
        self.endpoint = endpoint
        self.access_key = os.getenv("MINIO_ROOT_USER", "admin_minio")
        self.secret_key = os.getenv("MINIO_ROOT_PASSWORD", "minio_dev_pass")
        self.bucket_name = bucket_name
        
        # En docker-compose usaremos secure=False porque no hay SSL para la red interna
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False
        )
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' creado exitosamente en MinIO.")
        except S3Error as e:
            logger.error(f"Error asegurando el bucket MinIO: {e}")

    def upload_file(self, file_data, file_name: str, content_type: str, file_size: int = -1) -> str:
        """Sube un archivo a MinIO y devuelve su object_name (key)"""
        try:
            # Minio requiere el length del stream (file_size). Si conocemos filesize mejor, o pasamos el length del bytearray
            # Usualmente en FastApi upload file podemos obtener la longitud con len(data) o iterando el stream
            if file_size == -1:
                file_size = len(file_data.read())
                file_data.seek(0)
                
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_name,
                data=file_data,
                length=file_size,
                content_type=content_type
            )
            logger.info(f"Archivo {file_name} subido exitosamente a MinIO.")
            return file_name
        except S3Error as e:
            logger.error(f"Error subiendo el archivo {file_name} a MinIO: {e}")
            raise e

    def get_presigned_url(self, file_name: str, expiration_hours: int = 24) -> str:
        """Genera una Presigned URL (GET) válida por un tiempo determinado."""
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=file_name,
                expires=timedelta(hours=expiration_hours)
            )
            return url
        except S3Error as e:
            logger.error(f"Error generando presigned URL para {file_name}: {e}")
            raise e
