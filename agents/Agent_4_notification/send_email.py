import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(recipient: str, subject: str, body: str) -> bool:
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    
    if not sender_email or not sender_password:
        return True
    
    try:
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True
        
    except Exception as e:
        return False
