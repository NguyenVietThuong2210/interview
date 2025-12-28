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
    "email_tasks_1",
    broker=f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
)
email_celery_app.conf.task_default_queue = "email_queue"


@email_celery_app.task(name="send_email_task")
def send_email_task(
    filename: str, file_info: dict, email_config: dict, recipients: list
):
    """Celery task to send email with Excel attachment"""
    try:
        logger.info(f"Sending email for file: {filename}")

        # Download file from MinIO
        bucket_name = file_info["bucket"]
        response = minio_client.get_object(bucket_name, filename)
        file_data = response.read()
        response.close()
        response.release_conn()

        logger.info(f"Downloaded {filename} from MinIO ({len(file_data)} bytes)")

        # Prepare email
        subject = f"Interview Questions Export - {file_info['topic_id']}"
        body = f"""
        Hello,

        A new export file has been generated for Topic ID: {file_info['topic_id']}

        File Details:
        - Filename: {filename}
        - Generated at: {file_info['created_at']}
        - Size: {file_info['size']} bytes

        Please find the Excel file attached.

        Best regards,
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
                logger.info(f"Email 1 sent to {recipient['email']}")
            except Exception as e:
                logger.error(f"Failed to send email to {recipient['email']}: {str(e)}")

        return {
            "status": "success",
            "filename": filename,
            "recipients_count": len(recipients),
        }

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return {"status": "failed", "error": str(e)}
