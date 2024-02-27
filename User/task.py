from celery import Celery
from User.setting import redis_url
import smtplib, ssl
from email.message import EmailMessage
from User.setting import email_sender, email_password

celery = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    broker_connection_retry_on_startup=True
)

mail = EmailMessage()


# @celery.task()
def email_notification(recipient, message, subject):
    mail['From'] = email_sender
    mail['To'] = recipient
    mail['Subject'] = subject

    mail.set_content(message)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, recipient, mail.as_string())
        smtp.quit()
    return f"{recipient} mail send Successfully"

# celery -A task.celery worker -l info --pool=solo
