from datetime import datetime
import pika
import json
import logging

from shared.settings import RABBITMQ_EXPORT_QUEUE, RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER

logger = logging.getLogger(__name__)

class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()
    
    def connect(self):
        """Connect to RabbitMQ"""
        credentials = pika.PlainCredentials(
            RABBITMQ_USER,
            RABBITMQ_PASS
        )
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare queue
        self.channel.queue_declare(
            queue=RABBITMQ_EXPORT_QUEUE,
            durable=True
        )
    
    def send_export_message(self, topic_id: int, action: str = "export"):
        """Send message to export service"""
        message = {
            "topic_id": topic_id,
            "action": action,
            "timestamp": str(datetime.utcnow())
        }
        
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_EXPORT_QUEUE,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            logger.info(f"Sent export message for topic {topic_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")
            self.connect()  # Reconnect
            return False
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()

rabbitmq_service = RabbitMQService()