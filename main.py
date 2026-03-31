import imaplib
import email
from email.header import decode_header
import requests
import time
import os

# ===== Environment Variables =====
EMAIL = os.environ['pagoldarsanik@gmail.com']
APP_PASSWORD = os.environ['zxat jbhj ejks nlqv']
BOT_TOKEN = os.environ['8075761114:AAH-1OlKoUwEZbnpl-pDj0S-GL66gGVrlH0']
CHAT_ID = os.environ['7355153180']
# =================================

def decode_text(text):
    if text is None:
        return "No Data"
    decoded, charset = decode_header(text)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8", errors="ignore")
    return decoded

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })
    print("Telegram Response:", res.text)

def check_mail():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        mail_ids = messages[0].split()

        if not mail_ids:
            print("No new emails")
            return

        for num in mail_ids:
            status, msg_data = mail.fetch(num, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject = decode_text(msg["subject"])
                    from_ = decode_text(msg["from"])
                    text = f"""📩 NEW EMAIL

👤 From: {from_}
📝 Subject: {subject}
"""
                    send_telegram(text)
                    print("Sent:", subject)

        mail.logout()
    except Exception as e:
        print("ERROR:", e)

# ===== Main loop =====
while True:
    print("Checking Gmail...")
    check_mail()
    time.sleep(60)  # প্রতি ১ মিনিটে চেক করবে
