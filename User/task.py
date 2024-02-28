from celery import Celery
import smtplib, ssl
from email.message import EmailMessage
from User.setting import setting

celery = Celery(
    __name__,
    broker=setting.redis_url,
    backend=setting.redis_url,
    broker_connection_retry_on_startup=True
)

mail = EmailMessage()


@celery.task()
def email_notification(recipient, message, subject):
    mail['From'] = setting.email_sender
    mail['To'] = recipient
    mail['Subject'] = subject

    mail.set_content(message)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(setting.email_sender, setting.email_password)
        smtp.sendmail(setting.email_sender, recipient, mail.as_string())
        smtp.quit()
    return f"{recipient} mail send Successfully"

# celery -A task.celery worker -l info --pool=solo
