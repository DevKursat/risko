import smtplib
from email.mime.text import MIMEText
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def send_password_reset_email(to_email: str, token: str):
    frontend = settings.FRONTEND_BASE_URL or ""
    link = f"{frontend.rstrip('/')}/reset.html?token={token}" if frontend else f"/reset.html?token={token}"
    subject = "Risko - Şifre Sıfırlama"
    body = f"Merhaba,\n\nŞifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n{link}\n\nEğer bu talebi siz yapmadıysanız, bu e-postayı yok sayabilirsiniz.\n\nRisko Platform"

    if not settings.SMTP_HOST:
        # SMTP yoksa logla/print et (dev için)
        logger.info("[DEV] Password reset link for %s: %s", to_email, link)
        return True

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USERNAME or "no-reply@risko"
        msg["To"] = to_email

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587)
        if settings.SMTP_TLS:
            server.starttls()
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        logger.error("Failed to send reset email: %s", e)
        return False