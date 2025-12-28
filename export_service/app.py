import asyncio
from datetime import datetime
import json
import aio_pika
import logging
import orjson
from shared.services.redis_service import redis_service
from shared.settings import (
    EMAIL_SERVICE_2_HOST,
    EMAIL_SERVICE_2_PORT,
    MAX_READ_BYTES,
    RABBITMQ_EXPORT_QUEUE,
    RABBITMQ_HOST,
    RABBITMQ_PASS,
    RABBITMQ_PORT,
    RABBITMQ_USER,
)


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue = None

    async def connect(self):
        """Connect to RabbitMQ"""
        connection_url = (
            f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
        )
        logger.info(f"Connecting to RabbitMQ: {connection_url}")
        self.connection = await aio_pika.connect_robust(connection_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        self.queue = await self.channel.declare_queue(
            RABBITMQ_EXPORT_QUEUE, durable=True
        )
        logger.info(
            f"Connected to RabbitMQ, listening on queue: {RABBITMQ_EXPORT_QUEUE}"
        )

    async def send_to_email_service_2(self, payload: dict):
        """Send payload to Email Service 2 via TCP"""
        try:
            reader, writer = await asyncio.open_connection(
                EMAIL_SERVICE_2_HOST, EMAIL_SERVICE_2_PORT
            )

            # Send payload
            message = orjson.dumps(payload)
            writer.write(message)
            await writer.drain()

            # Read response
            response = await reader.read(MAX_READ_BYTES)
            result = response.decode()
            logger.info(f"Email Service 2 response: {result}")
            writer.close()
            await writer.wait_closed()

            return result == "ok"

        except Exception as e:
            logger.error(f"Failed to send to Email Service 2: {str(e)}")
            return False

    async def handle_message(self, message: aio_pika.IncomingMessage):
        """Handle incoming message from RabbitMQ"""
        async with message.process():
            try:
                payload = orjson.loads(message.body)
                topic_id = payload.get("topic_id")
                action = payload.get("action", "export")

                logger.info(f"Received message: topic_id={topic_id}, action={action}")

                # Call async version directly (don't use to_thread)
                succeeded = await self.handle_export_async(payload)

                if succeeded:
                    logger.info(f"Successfully processed topic {topic_id}")
                else:
                    logger.error(f"Failed to process topic {topic_id}")

            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")

    async def handle_export_async(self, payload: dict) -> bool:
        """Handle export logic"""
        try:
            topic_id = payload.get("topic_id")

            # Get data from Redis
            data = redis_service.client.get(f"topic:question:{topic_id}")
            if not data:
                logger.warning(f"No data found in Redis for topic {topic_id}")
                return False

            topic_data = json.loads(data)

            # Create Celery task for Excel generation
            from export_service.tasks import generate_excel_task

            result = generate_excel_task.delay(topic_data)

            # Wait for task to complete (or use result.get() with timeout)
            task_result = result.get(timeout=30)
            logger.info(f"Celery task for Excel generation: {task_result['status']}")

            if task_result["status"] == "success":
                filename = task_result["filename"]

                # 1. Mark in Redis for Email Service 1
                redis_service.client.sadd("files:new", filename)
                logger.info(f"Marked {filename} in Redis for Email Service 1")

                # 2. Send payload to Email Service 2 via TCP
                email_payload = {
                    "filename": filename,
                    "topic_id": topic_id,
                    "bucket": task_result.get("bucket", "exports"),
                    "size": task_result["size"],
                    "timestamp": str(datetime.utcnow()),
                }

                # Create task to send to Email Service 2 (fire and forget)
                asyncio.create_task(self.send_to_email_service_2(email_payload))
                logger.info(f"→ TCP: {filename} (for Email Service 2)")

                return True

            return False

        except Exception as e:
            logger.error(f"Error in handle_export_async: {str(e)}")
            return False

    async def start_consuming(self):
        """Start consuming messages"""
        await self.connect()
        await self.queue.consume(self.handle_message)
        logger.info("Started consuming messages...")


async def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Starting Export Service...")
    logger.info(f"RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    logger.info(f"Email Service 2: {EMAIL_SERVICE_2_HOST}:{EMAIL_SERVICE_2_PORT}")
    logger.info("=" * 60)

    export_service = ExportService()

    try:
        await export_service.start_consuming()
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
