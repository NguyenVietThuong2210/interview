from email.message import EmailMessage
from email.utils import formataddr
import mimetypes
import smtplib

def send_email_with_attachment(
    recipient_email: str,
    recipient_name: str,
    subject: str,
    body: str,
    attachment_data: bytes,
    attachment_filename: str,
    email_config: dict
):
    """
    Send email with attachment using SMTP (SendGrid compatible)
    """
    # Create email
    msg = EmailMessage()
    msg["From"] = formataddr((
        email_config.get("from_name", ""),
        email_config["from_email"]
    ))
    msg["To"] = formataddr((recipient_name, recipient_email))
    msg["Subject"] = subject

    # Email body (HTML + fallback text)
    msg.set_content(body)
    msg.add_alternative(body, subtype="html")

    # Guess MIME type
    mime_type, _ = mimetypes.guess_type(attachment_filename)
    if mime_type:
        maintype, subtype = mime_type.split("/", 1)
    else:
        maintype, subtype = "application", "octet-stream"

    # Add attachment
    msg.add_attachment(
        attachment_data,
        maintype=maintype,
        subtype=subtype,
        filename=attachment_filename
    )

    # Send email
    with smtplib.SMTP(
        email_config["smtp_host"],
        email_config["smtp_port"]
    ) as server:
        server.starttls()
        server.login(
            email_config["smtp_user"],
            email_config["smtp_password"]
        )
        server.send_message(msg)