import asyncio
import json
import logging
from shared.services.redis_service import redis_service
from shared.settings import MINIO_HOST, REDIS_HOST, REDIS_PORT

CHECK_INTERVAL = 10  # Check every 10 seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [EMAIL-1] - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EmailService1:
    def __init__(self):
        self.running = True
        self.processed_files = set()

    async def check_new_files(self):
        """Check for new files in MinIO"""
        try:
            # Get list of new files from Redis
            new_files = redis_service.client.smembers("files:new")

            if new_files:
                logger.info(f"Found {len(new_files)} new files to process")

                for filename in new_files:
                    if filename not in self.processed_files:
                        # Process in thread to avoid blocking
                        succeeded = await asyncio.to_thread(
                            self.handle_new_file, filename
                        )

                        if succeeded:
                            self.processed_files.add(filename)
                            logger.info(f"Successfully processed {filename}")
                        else:
                            logger.error(f"Failed to process {filename}")

        except Exception as e:
            logger.error(f"Error checking new files: {str(e)}")

    def handle_new_file(self, filename: str) -> bool:
        """Handle new file detection (runs in thread)"""
        try:
            logger.info(f"Processing new file: {filename}")

            # Get file metadata from Redis
            metadata_key = f"file:metadata:{filename}"
            metadata = redis_service.client.get(metadata_key)

            if not metadata:
                logger.warning(f"No metadata found for {filename}")
                return False

            file_info = json.loads(metadata)

            # Get email config from Redis
            email_config = redis_service.client.get("email:config")
            if not email_config:
                logger.error("No email config found in Redis")
                return False

            email_config = json.loads(email_config)

            # Get admin users from Redis
            admin_users = redis_service.client.get("admin:users")
            if not admin_users:
                logger.error("No admin users found in Redis")
                return False

            admin_users = json.loads(admin_users)

            # Create Celery task to send email
            from email_service_1.tasks import send_email_task

            task = send_email_task.delay(
                filename=filename,
                file_info=file_info,
                email_config=email_config,
                recipients=admin_users,
            )

            logger.info(f"Created Celery task {task.id} to send email for {filename}")

            # Mark file as processed in Redis
            redis_service.client.srem("files:new", filename)
            redis_service.client.sadd("files:processed:service1", filename)

            return True

        except Exception as e:
            logger.error(f"Error in handle_new_file: {str(e)}")
            return False

    async def run_loop(self):
        """Main service loop"""
        logger.info("Starting Email Service main loop...")

        while self.running:
            try:
                # Check for new files
                await self.check_new_files()

                # Wait before next check
                await asyncio.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                logger.info("Service stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                await asyncio.sleep(CHECK_INTERVAL)


async def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("Starting Email Service...")
    logger.info(f"MinIO Host: {MINIO_HOST}")
    logger.info(f"Redis Host: {REDIS_HOST}:{REDIS_PORT}")
    logger.info(f"Check Interval: {CHECK_INTERVAL} seconds")
    logger.info("=" * 60)

    email_service = EmailService1()

    try:
        await email_service.run_loop()
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
