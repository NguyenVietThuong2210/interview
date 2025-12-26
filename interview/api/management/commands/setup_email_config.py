from django.core.management.base import BaseCommand
from .....shared.services import redis_service

class Command(BaseCommand):
    help = 'Setup email configuration in Redis'
    
    def handle(self, *args, **options):
        # Email configuration
        email_config = {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_user": "your-email@gmail.com",
            "smtp_password": "your-app-password",
            "from_email": "noreply@interview-api.com",
            "from_name": "Interview API"
        }
        redis_service.save_email_config(email_config)
        
        # Admin users
        admin_users = [
            {
                "email": "nguyenvietthuong0922@gmail.com",
                "name": "Admin User"
            }
        ]
        redis_service.save_admin_users(admin_users)
        self.stdout.write(self.style.SUCCESS('Email config saved to Redis'))