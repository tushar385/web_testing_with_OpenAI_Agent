import os
import datetime

LOG_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_FOLDER, "user_logs.txt")

def ensure_log_folder():
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

def clear_logs():
    ensure_log_folder()
    with open(LOG_FILE, "w") as f:
        f.write("")

def log_message(message):
    ensure_log_folder()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def read_logs():
    ensure_log_folder()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    return []

def initialize_logs():
    clear_logs()