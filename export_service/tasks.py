import json
import logging
from shared.services.redis_service import redis_service
from .app import celery_app
from shared.minio import minio_client
from datetime import datetime
from shared.services.excel_generator import ExcelGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@celery_app.task(name='generate_excel_task')
def generate_excel_task(topic_data: dict):
    """Generate Excel and upload to MinIO"""
    try:
        topic_id = topic_data['topic_id']
        questions = topic_data['questions']
        
        logger.info(f"Generating Excel for topic {topic_id}")
        
        # Generate Excel
        generator = ExcelGenerator()
        excel_bytes = generator.generate(topic_id, questions)
        
        # Generate filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"export_topic_{topic_id}_{timestamp}.xlsx"
        
        # Upload to MinIO
        bucket_name = "exports"
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        
        from io import BytesIO
        excel_stream = BytesIO(excel_bytes)
        minio_client.put_object(
            bucket_name,
            filename,
            excel_stream,
            length=len(excel_bytes),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        logger.info(f"Uploaded {filename} to MinIO")
        
        # Save metadata to Redis
        file_metadata = {
            "filename": filename,
            "bucket": bucket_name,
            "topic_id": topic_id,
            "created_at": timestamp,
            "size": len(excel_bytes)
        }
        redis_service.client.set(f"file:metadata:{filename}", json.dumps(file_metadata))
        
        return {
            "status": "success",
            "filename": filename,
            "bucket": bucket_name,
            "size": len(excel_bytes)
        }
        
    except Exception as e:
        logger.error(f"Error generating Excel: {str(e)}")
        return {
            "status": "failed",
            "error": str(e)
        }