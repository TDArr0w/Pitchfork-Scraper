import socket
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

env_path = Path(".env")
env_vars = {}
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

EMAIL = env_vars.get("email")
PASSWORD = env_vars.get("password")

# SMTP settings for Outlook
PORT = 587
SMTP_SERVER = "smtp.gmail.com"

# Use getaddrinfo to resolve the SMTP server address
try:
    addr_info = socket.getaddrinfo(SMTP_SERVER, PORT, proto=socket.IPPROTO_TCP)
    print(f"Resolved address info for {SMTP_SERVER}: {addr_info}")
except Exception as e:
    print(f"Error resolving address for {SMTP_SERVER}: {e}")


def send_email(subject: str, recipient: str, name: str, body_text: str = None, body_html: str = None):
    """
    Send an email using the configured SMTP server.

    Args:
        subject (str): Subject line of the email.
        recipient (str): Receiver email address.
        name (str): Name of the recipient for personalization.
        body_text (str, optional): Plaintext email body.
        body_html (str, optional): HTML email body.
    """

    if not EMAIL or not PASSWORD:
        raise ValueError("Missing EMAIL or PASSWORD in environment variables")

    # Fallback text if nothing is passed
    if not body_text:
        body_text = f"Hi {name},\n\nA new album has been found on Pitchfork!\n\nCheck it out!"

    if not body_html:
        body_html = f"""
        <!DOCTYPE html>
        <html>
            <body>
                <p>Hi {name},</p>
                <p>A new album has been found on Pitchfork!</p>
                <p>Check it out!</p>
            </body>
        </html>
        """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Pitchfork Scraper", EMAIL))
    msg["To"] = recipient
    msg["BCC"] = EMAIL  # keep a copy
    msg.set_content(body_text)
    msg.add_alternative(body_html, subtype="html")

    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"email: {EMAIL}, password: {PASSWORD}")
        print(f"Error sending email: {e}")



    # Example usage
send_email(
    subject="Test Email",
    recipient="theoaronow@gmail.com",
    name="Theo")