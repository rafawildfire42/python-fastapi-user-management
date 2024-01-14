from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib

from fastapi.responses import JSONResponse
from fastapi import status


def send_email(receiver: str):
    try:
        me = config("EMAIL_SENDER")
        you = receiver

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Olá, confirme o seu cadastro!"
        msg["From"] = me
        msg["To"] = you

        HTMLFile = open("templates/confirm_register.html", "r")

        html = HTMLFile.read()
        html = html.replace(
            "{{button}}",
            f'<a class="button" href="http://localhost:8000/confirm-register?email={receiver}">Confirmar cadastro</a>',
        )
        HTMLFile.close()

        html_content = MIMEText(html, "html")

        msg.attach(html_content)

        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(me, config("EMAIL_PASSWORD"))
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Error while sending email."},
        )
