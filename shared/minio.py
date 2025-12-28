from minio import Minio
from shared.settings import MINIO_ACCESS_KEY, MINIO_HOST, MINIO_SECRET_KEY

# MinIO client
minio_client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)