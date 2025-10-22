from fastapi import BackgroundTasks
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

# Load email templates from app/templates/
env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "../templates")))

SMTP_SERVER = "smtp.gmail.com"  # or your email server
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"      # sender email
EMAIL_PASSWORD = "your_app_password_here"   # app password (not your normal Gmail password)

def send_email(to_email: str, subject: str, template_name: str, context: dict):
    template = env.get_template(template_name)
    body = template.render(context)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"Email sent to {to_email}")

def send_email_background(background_tasks: BackgroundTasks, to_email: str, subject: str, template_name: str, context: dict):
    background_tasks.add_task(send_email, to_email, subject, template_name, context)

def send_volunteer_notification(to_email: str, context: dict):
    send_email(
        to_email,
        subject="Volunteer Notification",
        template_name="volunteer_notification.html",
        context=context
    )

def send_donor_confirmation(to_email: str, context: dict):
    send_email(
        to_email,
        subject="Donation Confirmation",
        template_name="donor_confirmation.html",
        context=context
    )

def send_admin_alert(to_email: str, context: dict):
    send_email(
        to_email,
        subject="Admin Alert: New Update",
        template_name="admin_alert.html",
        context=context
    )
