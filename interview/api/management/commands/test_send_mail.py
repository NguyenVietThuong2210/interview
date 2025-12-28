from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from django.core.management.base import BaseCommand
from shared.services.redis_service import redis_service

class Command(BaseCommand):
    help = 'Setup email configuration in Redis'
    
    def handle(self, *args, **options):
        email_config = redis_service.get_email_config()
        SMTP_SERVER = email_config["smtp_host"]
        SMTP_PORT = email_config["smtp_port"]
        SMTP_USER = email_config["smtp_user"]
        SMTP_PASSWORD = email_config["smtp_password"]
        from_email = email_config["from_email"]
        print("1\ Sending test email via SendGrid SMTP...")
        print(f"SMTP Server: {SMTP_SERVER}")
        print(f"Port: {SMTP_PORT}")
        print(f"User: {SMTP_USER}")
        print(f"Password: {SMTP_PASSWORD}")
        print(f"From Email: {from_email}")

        message = Mail(
            from_email=from_email,
            to_emails="nguyenvietthuong0922@gmail.com",
            subject="subject",
            plain_text_content="content",
        )

        sg = SendGridAPIClient(api_key=SMTP_PASSWORD)
        response = sg.send(message)
        print("Email sent! Status code:", response.status_code)