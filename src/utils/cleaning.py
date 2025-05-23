def format_decimal(value):
    """
    Format a decimal value to two decimal places.
    """
    if isinstance(value, str):
        value = value.replace(',', '.')
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return None