from typing import BinaryIO
import uuid
from minio import Minio
from app.core.exceptions import StorageError

class StorageService:
    def __init__(self, config):
        self.client = Minio(
            config.get('MINIO_ENDPOINT'),
            access_key=config.get('MINIO_ACCESS_KEY'),
            secret_key=config.get('MINIO_SECRET_KEY'),
            secure=False
        )
        self.bucket_name = config.get('MINIO_BUCKET_NAME')
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def generate_storage_path(self, filename: str) -> str:
        ext = filename.rsplit('.', 1)[-1].lower()
        return f"videos/{uuid.uuid4()}.{ext}"

    def upload_file(self, file_obj: BinaryIO, storage_path: str) -> str:
        try:
            file_size = file_obj.tell()
            file_obj.seek(0)
            
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=storage_path,
                data=file_obj,
                length=file_size
            )
            return storage_path
        except Exception as e:
            raise StorageError(f"Failed to upload file: {str(e)}")

    def delete_file(self, storage_path: str) -> None:
        try:
            self.client.remove_object(self.bucket_name, storage_path)
        except Exception as e:
            raise StorageError(f"Failed to delete file: {str(e)}")

    def get_file_url(self, storage_path: str, expires=3600) -> str:
        try:
            return self.client.presigned_get_object(
                self.bucket_name,
                storage_path,
                expires=expires
            )
        except Exception as e:
            raise StorageError(f"Failed to generate URL: {str(e)}")
