import imaplib
import email
from email.header import decode_header
import requests
import time

# ==========================
# Telegram Settings
# ==========================
BOT_TOKEN = "8676092689:AAFFly55LiT4rhQ-Z-uAmP5gP8r4Wx71MZU"
CHAT_ID = "7799924845"

# ==========================
# Gmail Accounts
# Format: "email@gmail.com": "app_password"
# ==========================
ACCOUNTS = {
    "paneL12345g@gmail.com": "fmts iyih pzkb jcea",
    "mdsohag3992@gmail.com": "nkpd ydfv tply qpny",
    "mpaleologoSmatthew@gmail.com": "mtvj vnva ghik ibmy",
    "mondaldiku7@gmail.com": "yolc iwtc kjng iqwt",
    "claudettespencer45@gmail.com": "eftz dmvz aasd jmkz",
    "email6@gmail.com": "app_pass6",
    "email7@gmail.com": "app_pass7",
    "email8@gmail.com": "app_pass8",
    "email9@gmail.com": "app_pass9",
    "email10@gmail.com": "app_pass10",
}

# ==========================
# Track last seen email per account
# ==========================
last_seen_ids = {}

# ==========================
# Telegram Sender
# ==========================
def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# ==========================
# Decode Email Header
# ==========================
def decode_text(text):
    if text is None:
        return "No Subject"
    decoded, charset = decode_header(text)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8", errors="ignore")
    return decoded

# ==========================
# Check New Emails
# ==========================
def check_mail(email_addr, app_pass):
    global last_seen_ids
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_pass)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        if not mail_ids:
            mail.logout()
            return

        latest_id = mail_ids[-1]

        # প্রথমবার run হলে শুধু latest save করবে, send করবে না
        if email_addr not in last_seen_ids:
            last_seen_ids[email_addr] = latest_id
            print(f"[{email_addr}] Initialized. Waiting for new mails...")
            mail.logout()
            return

        new_mails = [num for num in mail_ids if int(num) > int(last_seen_ids[email_addr])]

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
💌 Gmail: {email_addr}
"""
                    send_telegram(text)
                    print(f"[{email_addr}] Sent: {subject}")

        last_seen_ids[email_addr] = latest_id
        mail.logout()

    except Exception as e:
        print(f"[{email_addr}] ERROR:", e)

# ==========================
# Bot Startup Notification
# ==========================
send_telegram("🤖 Multi-Gmail Bot is now RUNNING! Waiting for new emails...")

# ==========================
# Main Loop
# ==========================
while True:
    for email_addr, app_pass in ACCOUNTS.items():
        check_mail(email_addr, app_pass)
    time.sleep(5)  # প্রতি ১ মিনিটে চেক করবে
