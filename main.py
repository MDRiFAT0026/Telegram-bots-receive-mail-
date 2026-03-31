import imaplib
import email
from email.header import decode_header
import requests
import time
import os

EMAIL = os.environ['pagoldarsanik@gmail.com']  # তোমার Gmail
APP_PASSWORD = os.environ['zxat jbhj ejks nlqv']  # Gmail app password
BOT_TOKEN = os.environ['8075761114:AAH-1OlKoUwEZbnpl-pDj0S-GL66gGVrlH0']
CHAT_ID = os.environ['7355153180']

last_seen_id = None  # নতুন mail track করার জন্য

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

def decode_text(text):
    if text is None:
        return "No Subject"
    decoded, charset = decode_header(text)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8", errors="ignore")
    return decoded

def check_mail():
    global last_seen_id

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    if not mail_ids:
        return

    latest_id = mail_ids[-1]

    # প্রথমবার run হলে শুধু latest save করবে, send করবে না
    if last_seen_id is None:
        last_seen_id = latest_id
        print("Initialized. Waiting for new mails...")
        return

    new_mails = [num for num in mail_ids if int(num) > int(last_seen_id)]

    for num in new_mails:
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

    last_seen_id = latest_id
    mail.logout()

# 🔔 Bot Startup Notification
send_telegram("🤖 Bot is now ONLINE! Waiting for new emails...")

while True:
    try:
        check_mail()
    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)  # প্রতি ১ মিনিটে চেক করবে
