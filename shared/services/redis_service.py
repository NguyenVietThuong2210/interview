from datetime import datetime
import redis
import json
from typing import Dict, List, Optional
from shared.settings import REDIS_DB, REDIS_HOST, REDIS_PORT

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
    
    def save_topic_question_data(self, topic_id: int, questions: List[Dict]):
        """Save topic-question data to Redis"""
        key = f"topic:question:{topic_id}"
        data = {
            "topic_id": topic_id,
            "questions": questions,
            "timestamp": str(datetime.utcnow())
        }
        self.client.set(key, json.dumps(data))
        
        # Also maintain a list of all topic IDs
        self.client.sadd("topics:all", topic_id)
        
        return key
    
    def get_topic_question_data(self, topic_id: int) -> Optional[Dict]:
        """Get topic-question data from Redis"""
        key = f"topic:question:{topic_id}"
        data = self.client.get(key)
        return json.loads(data) if data else None
    
    def get_all_topics_questions(self) -> List[Dict]:
        """Get all topics and questions"""
        topic_ids = self.client.smembers("topics:all")
        all_data = []
        for topic_id in topic_ids:
            data = self.get_topic_question_data(int(topic_id))
            if data:
                all_data.append(data)
        return all_data
    
    def save_email_config(self, config: Dict):
        """Save email configuration"""
        self.client.set("email:config", json.dumps(config))
    
    def get_email_config(self) -> Optional[Dict]:
        """Get email configuration"""
        data = self.client.get("email:config")
        return json.loads(data) if data else None
    
    def save_admin_users(self, users: List[Dict]):
        """Save admin users info"""
        self.client.set("admin:users", json.dumps(users))
    
    def get_admin_users(self) -> List[Dict]:
        """Get admin users info"""
        data = self.client.get("admin:users")
        return json.loads(data) if data else []
    
    def mark_file_as_new(self, filename: str):
        """Mark Excel file as new (for email service to detect)"""
        self.client.sadd("files:new", filename)
    
    def get_new_files(self) -> List[str]:
        """Get list of new files"""
        return list(self.client.smembers("files:new"))
    
    def mark_file_as_processed(self, filename: str):
        """Mark file as processed"""
        self.client.srem("files:new", filename)
        self.client.sadd("files:processed", filename)

redis_service = RedisService()