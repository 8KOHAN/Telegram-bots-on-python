from datetime import datetime

def format_datetime_for_user(iso_str: str) -> str:
    """Форматує ISO дату у вигляді DD.MM о HH:MM"""
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d.%m о %H:%M")
    except Exception:
        return iso_str  # fallback
