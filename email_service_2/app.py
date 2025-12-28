import asyncio
import orjson
import redis
import json
import logging

from shared.services.redis_service import redis_service
from shared.settings import (
    EMAIL_SERVICE_2_HOST,
    EMAIL_SERVICE_2_PORT,
    EMAIL_SERVICE_2_SOCKET_BACKLOG,
    MAX_READ_BYTES,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [EMAIL-2] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def handle_client(reader, writer):
    """Handle TCP client connection"""
    addr = writer.get_extra_info("peername")
    logger.info(f"Connection from {addr}")

    try:
        # Read payload
        _payload = await reader.read(MAX_READ_BYTES)
        payload = orjson.loads(_payload)

        logger.info(f"Received payload: {payload.get('filename')}")

        # Process in thread
        succeeded = await asyncio.to_thread(handle, payload)

        # Send response
        ret = "ok" if succeeded else "nok"
        writer.write(ret.encode())
        await writer.drain()

        logger.info(f"Response: {ret}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        writer.write(b"nok")
        await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()


def handle(payload: dict) -> bool:
    """Handle payload"""
    try:
        filename = payload.get("filename")
        topic_id = payload.get("topic_id")
        bucket = payload.get("bucket", "exports")

        logger.info(f"Processing new file: {filename}")

        # Get email config
        email_config = redis_service.client.get("email:config")
        if not email_config:
            logger.error("No email config")
            return False
        email_config = json.loads(email_config)

        # Get admin users from Redis
        admin_users = redis_service.client.get("admin:users")
        if not admin_users:
            logger.error("No admin users found in Redis")
            return False

        admin_users = json.loads(admin_users)
        
        # File info
        file_info = {
            "filename": filename,
            "bucket": bucket,
            "topic_id": topic_id,
            "size": payload.get("size", 0),
            "created_at": payload.get("timestamp"),
        }

        # Create Celery task
        from email_service_2.tasks import send_email_task

        task = send_email_task.delay(
            filename=filename,
            file_info=file_info,
            email_config=email_config,
            recipients=admin_users,
            service_id=2,
        )

        logger.info(f"Created task {task.id}")

        # Mark as processed
        redis_service.client.sadd("files:processed:service2", filename)

        return True

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False


async def main():
    """Start TCP server"""
    logger.info("=" * 60)
    logger.info("[EMAIL SERVICE 2] Starting TCP Server...")
    logger.info(f"Host: {EMAIL_SERVICE_2_HOST}")
    logger.info(f"Port: {EMAIL_SERVICE_2_PORT}")
    logger.info(f"Backlog: {EMAIL_SERVICE_2_SOCKET_BACKLOG}")
    logger.info("=" * 60)
    server = await asyncio.start_server(
        handle_client,
        EMAIL_SERVICE_2_HOST,
        EMAIL_SERVICE_2_PORT,
        backlog=EMAIL_SERVICE_2_SOCKET_BACKLOG,
    )

    async with server:
        addr = server.sockets[0].getsockname()
        logger.info(f"TCP Server running on {addr[0]}:{addr[1]}")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
