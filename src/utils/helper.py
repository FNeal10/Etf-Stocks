import os
from datetime import datetime


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
log_dir_path = os.path.join(root_dir, "logs")
filename = "log_" + datetime.now().strftime("%m%d%Y") + ".log"
log_file_path = os.path.join(log_dir_path, filename)

def format_to_decimal(value):
    """
    Format a decimal value to two decimal places.
    Removes commas and handles errors safely.
    """
    if isinstance(value, str):
        value = value.replace(',', '').replace('"',"").replace("'","")  # Remove thousands separator
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        print(value)
        return None


def check_or_create_logfile():
    """
    Ensure today's log file exists in the given log directory.
    If it doesn't exist, create it. Does not return anything.
    """
    os.makedirs(log_dir_path, exist_ok=True)    

    if not os.path.isfile(log_file_path):
        open(log_file_path, "w").close()

def append_to_log(message):
    """
    Append a message to the log file for today.
    """
    check_or_create_logfile()
    
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

