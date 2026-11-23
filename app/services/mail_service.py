import os
import smtplib
from email.message import EmailMessage
from fastapi import HTTPException, status


class MailService:
    def __init__(
        self,
        use_tls: bool | None = None,
    ) -> None:
        self.host = os.getenv("SMTP_HOST")
        self.port = os.getenv("SMTP_PORT")
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.default_from = os.getenv("MAIL_FROM")
        env_tls = os.getenv("SMTP_USE_TLS", "true")
        self.use_tls = env_tls.lower() in ("1", "true", "yes")

    def send_mail(
        self,
        to: str | list[str],
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:

        recipients = ", ".join(to) if isinstance(to, list) else to
        if not recipients:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe especificarse al menos un destinatario.",
            )

        msg = EmailMessage()
        msg["From"] = self.default_from
        msg["To"] = recipients
        msg["Subject"] = subject

        # Contenido en texto plano (fallback)
        msg.set_content(text)

        # Contenido HTML opcional
        if html:
            msg.add_alternative(html, subtype="html")

        try:
            if self.use_tls:
                with smtplib.SMTP(self.host, self.port, timeout=15) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    if self.username and self.password:
                        server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP_SSL(self.host, self.port, timeout=15) as server:
                    if self.username and self.password:
                        server.login(self.username, self.password)
                    server.send_message(msg)
            return {"message": "Correo enviado exitosamente."}
        except smtplib.SMTPException as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error al enviar correo por SMTP: {exc}",
            ) from exc
        except OSError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"No se pudo conectar al servidor SMTP: {exc}",
            ) from exc