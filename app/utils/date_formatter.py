from datetime import datetime

def date_formatter(date_str):
    if isinstance(date_str, datetime):
        return date_str.strftime("%b %d %Y")
    return datetime.fromisoformat(date_str).strftime("%b %d %Y")
