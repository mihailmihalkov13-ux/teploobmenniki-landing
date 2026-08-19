import os
import smtplib
import re
from pathlib import Path
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.yandex.ru")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
LEAD_EMAIL_TO = os.environ.get("LEAD_EMAIL_TO")
PORT = int(os.environ.get("PORT", "5000"))

PHONE_RE = re.compile(r"^[\d\s()+\-]{5,20}$")

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/lead", methods=["POST"])
def submit_lead():
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()
    consent = data.get("consent")

    if not name or not phone:
        return jsonify({"ok": False, "error": "Укажите имя и телефон"}), 400
    if consent not in (True, "true", "on", "1", 1):
        return jsonify({"ok": False, "error": "Нужно согласие на обработку персональных данных"}), 400
    if len(name) > 200 or len(message) > 2000:
        return jsonify({"ok": False, "error": "Слишком длинное значение"}), 400
    if not PHONE_RE.match(phone):
        return jsonify({"ok": False, "error": "Некорректный телефон"}), 400

    if not SMTP_USER or not SMTP_PASSWORD or not LEAD_EMAIL_TO:
        app.logger.error("SMTP не настроен: проверьте .env")
        return jsonify({"ok": False, "error": "Сервис временно недоступен"}), 500

    body_lines = [
        "Новая заявка с сайта teploobmenniki-landing",
        "",
        f"Имя: {name}",
        f"Телефон: {phone}",
    ]
    if message:
        body_lines.append(f"Комментарий: {message}")

    email_msg = EmailMessage()
    email_msg["Subject"] = f"Заявка с сайта: {name}"
    email_msg["From"] = SMTP_USER
    email_msg["To"] = LEAD_EMAIL_TO
    email_msg["Reply-To"] = SMTP_USER
    email_msg["Date"] = formatdate(localtime=True)
    email_msg["Message-ID"] = make_msgid(domain=SMTP_USER.split("@")[-1])
    email_msg.set_content("\n".join(body_lines))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(email_msg)
    except Exception:
        app.logger.exception("Не удалось отправить письмо с заявкой")
        return jsonify({"ok": False, "error": "Не удалось отправить заявку"}), 502

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
