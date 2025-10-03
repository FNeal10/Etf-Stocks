import os
from datetime import datetime

def format_to_decimal(value):
    """
    Format a decimal value to two decimal places.
    Removes commas and handles errors safely.
    """
    if isinstance(value, str):
        value = value.replace(',', '').replace('"',"").replace("'","")
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        print(value)
        return None


