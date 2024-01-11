from celery import Celery
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi.responses import JSONResponse
from fastapi import status
from decouple import config

import os
import sys
import asyncio

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

rabbit_mq_host = config("RABBIT_MQ_HOST")


async def send_email(receiver: str):
    try:
        me = config("EMAIL_SENDER")
        you = receiver

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Olá, confirme o seu cadastro!"
        msg["From"] = me
        msg["To"] = you
        logging.info(project_path)
        logging.info(os.path.dirname(__file__))
        HTMLFile = open(
            "/app/src/apps/users/templates/confirm_register.html", "r")

        html = HTMLFile.read()
        html = html.replace(
            "{{button}}",
            f'<a class="button" href="http://localhost:8000/users/confirm-register?email={receiver}">Confirmar cadastro</a>',
        )
        HTMLFile.close()

        html_content = MIMEText(html, "html")

        msg.attach(html_content)

        logging.info("teste1")
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        logging.info("teste2")
        mail.ehlo()
        logging.info("teste3")
        mail.starttls()
        logging.info("teste4")
        mail.login(me, config("EMAIL_PASSWORD"))
        logging.info("teste5")
        mail.sendmail(me, you, msg.as_string())
        logging.info("teste6")
        mail.quit()
        logging.info("teste7")
    except Exception as e:
        print(e)
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Error while sending email."},
        )

print(rabbit_mq_host)
app = Celery('tasks', backend='rpc://',
             broker=f'pyamqp://guest@{rabbit_mq_host}//')
app.conf.update(imports=['users.crud'])


@app.task
def send_email_celery(receiver: str):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(send_email(receiver))
