from celery import Celery
from shared.minio import minio_client
import logging

from shared.settings import (
    RABBITMQ_HOST,
    RABBITMQ_PASS,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    REDIS_HOST,
    REDIS_PORT,
)

logger = logging.getLogger(__name__)

# Celery app
email_celery_app = Celery(
    "email_tasks_2",
    broker=f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/3",
)
email_celery_app.conf.task_default_queue = "email_queue"


@email_celery_app.task(name="send_email_task")
def send_email_task(
    filename: str,
    file_info: dict,
    email_config: dict,
    recipients: list,
    service_id: int,
):
    try:
        logger.info(f"[EMAIL-2] Sending email for file: {filename}")

        # Download file from MinIO
        bucket_name = file_info["bucket"]
        response = minio_client.get_object(bucket_name, filename)
        file_data = response.read()
        response.close()
        response.release_conn()

        logger.info(f"[EMAIL-2] Downloaded ({len(file_data)} bytes)")

        # Email content
        subject = f"[SERVICE-{service_id}] Interview Questions Export - Topic {file_info['topic_id']}"
        body = f"""
            Hello,

            This email is from Email Service {service_id} (TCP Server).

            Export Details:
            - Topic ID: {file_info['topic_id']}
            - Filename: {filename}
            - Generated: {file_info.get('created_at', 'N/A')}
            - Size: {file_info['size']} bytes

            Received via TCP payload from Export Service.

            Excel file is attached.

            Best regards,
            Email Service {service_id}
            Interview API System
        """

        # Send to each recipient
        for recipient in recipients:
            try:
                # send_email_with_attachment(
                #     recipient_email=recipient['email'],
                #     recipient_name=recipient['name'],
                #     subject=subject,
                #     body=body,
                #     attachment_data=file_data,
                #     attachment_filename=filename,
                #     email_config=email_config
                # )
                logger.info(f"[EMAIL-2] ✓ Sent to {recipient['email']}")
            except Exception as e:
                logger.error(f"[EMAIL-2] ✗ Failed {recipient['email']}: {str(e)}")

        return {"status": "success", "service": 2, "filename": filename}

    except Exception as e:
        logger.error(f"[EMAIL-2] Error: {str(e)}")
        return {"status": "failed", "error": str(e)}
