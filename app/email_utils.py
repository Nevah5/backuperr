import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

def send_error_email(subject, body):
    try:
        email_host = os.getenv('EMAIL_HOST')
        email_port = os.getenv('EMAIL_PORT')
        email_username = os.getenv('EMAIL_USERNAME')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_from = os.getenv('EMAIL_FROM')
        email_from_name = os.getenv('EMAIL_FROM_NAME', '')
        email_to = os.getenv('ERROR_EMAIL_TO')

        # Validate required environment variables
        if not all([email_host, email_port, email_username, email_password, email_from, email_to]):
            raise ValueError("Missing one or more required email environment variables.")

        email_port = int(email_port)  # Convert port to integer

        # Format the 'From' field with name if available
        formatted_email_from = f"{email_from_name} <{email_from}>" if email_from_name else email_from

        msg = MIMEMultipart()
        msg['From'] = formatted_email_from
        msg['To'] = email_to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.send_message(msg)

        print("Error email sent successfully.")
    except Exception as e:
        print(f"Failed to send error email: {e}")