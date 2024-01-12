from celery import Celery
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi.responses import JSONResponse
from fastapi import status
from decouple import config

import asyncio


rabbit_mq_host = config("RABBIT_MQ_HOST")


async def send_email(receiver: str):
    try:
        sender = config("EMAIL_SENDER")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Olá, confirme o seu cadastro!"
        msg["From"] = sender
        msg["To"] = receiver
        
        HTMLFile = open(
            "templates/confirm_register.html", "r")
        html = HTMLFile.read()
        html = html.replace(
            "{{button}}",
            f'<a class="button" href="http://localhost:8000/users/confirm-register?email={receiver}">Confirmar cadastro</a>',
        )
        HTMLFile.close()
        html_content = MIMEText(html, "html")
        msg.attach(html_content)

        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, config("EMAIL_PASSWORD"))
        mail.sendmail(sender, receiver, msg.as_string())
        mail.quit()
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Error while sending email."},
        )


app = Celery("tasks", backend="rpc://",
             broker=f"pyamqp://guest@{rabbit_mq_host}//")
app.config_from_object("src.apps.users.tasks", namespace="CELERY")

@app.task
def send_email_celery(receiver: str):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(send_email(receiver))
