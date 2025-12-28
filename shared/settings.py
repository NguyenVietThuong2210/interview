import os
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', default='redis')
REDIS_PORT = os.getenv('REDIS_PORT', default=6379)
REDIS_DB = os.getenv('REDIS_DB', default=0)

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', default='rabbitmq')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', default=5672)
RABBITMQ_USER = os.getenv('RABBITMQ_USER', default='guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', default='guest')
RABBITMQ_EXPORT_QUEUE = 'export_queue'
MAX_READ_BYTES = 1024 * 1024  # 1MB

EMAIL_SERVICE_2_HOST = os.getenv('EMAIL_SERVICE_2_HOST', default='email_service_2')
EMAIL_SERVICE_2_PORT = os.getenv('EMAIL_SERVICE_2_PORT', default=8888)
EMAIL_SERVICE_2_SOCKET_BACKLOG = 10

MINIO_HOST = "minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"