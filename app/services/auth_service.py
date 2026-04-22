import secrets
import smtplib
from email.message import EmailMessage
import os


def normalize_email(value):
    return str(value or "").strip().lower()


def password_policy_error(password):
    password = str(password or "")
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(ch.isalpha() for ch in password) or not any(ch.isdigit() for ch in password):
        return "Password must include both letters and numbers."
    return ""


def generate_reset_code(length=6):
    digits = "0123456789"
    return "".join(secrets.choice(digits) for _ in range(max(6, int(length))))


def generate_temporary_password(length=10):
    charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"
    return "".join(secrets.choice(charset) for _ in range(max(8, int(length))))


def send_password_reset_email(
    host,
    port,
    username,
    password,
    from_email,
    use_tls,
    to_email,
    code,
    role_label,
    account_name,
    ttl_minutes,
):
    message = EmailMessage()
    message["Subject"] = "DSEU Attendance Portal password reset code"
    message["From"] = from_email or username
    message["To"] = to_email
    message.set_content(
        (
            f"Hello {account_name or role_label},\n\n"
            f"Your one-time password reset code is: {code}\n"
            f"This code will expire in {ttl_minutes} minutes.\n\n"
            "If you did not request this reset, ignore this email.\n"
            "Do not share this code with anyone.\n"
        )
    )

    with smtplib.SMTP(host, int(port), timeout=20) as smtp:
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)


def smtp_settings_from_env():
    return {
        "host": os.getenv("SMTP_HOST", "").strip(),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "username": os.getenv("SMTP_USER", "").strip(),
        "password": os.getenv("SMTP_PASS", "").strip(),
        "from_email": os.getenv("SMTP_FROM_EMAIL", "").strip(),
        "use_tls": os.getenv("SMTP_USE_TLS", "1").strip() != "0",
    }
