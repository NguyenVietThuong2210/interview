import os
from dotenv import load_dotenv

load_dotenv()

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', default='redis')
REDIS_PORT = os.getenv('REDIS_PORT', default=6379, cast=int)
REDIS_DB = os.getenv('REDIS_DB', default=0, cast=int)

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', default='rabbitmq')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', default=5672, cast=int)
RABBITMQ_USER = os.getenv('RABBITMQ_USER', default='guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', default='guest')
RABBITMQ_EXPORT_QUEUE = 'export_queue'
MAX_READ_BYTES = 1024 * 1024  # 1MB

EMAIL_SERVICE_2_HOST = os.getenv('EMAIL_SERVICE_2_HOST', default='email_service_2')
EMAIL_SERVICE_2_PORT = os.getenv('EMAIL_SERVICE_2_PORT', default=9000)