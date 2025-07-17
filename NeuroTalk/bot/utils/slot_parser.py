from utils.formatting import format_datetime_for_user

def slots_to_text(slots: list[tuple[str, str]], limit: int = 5) -> str:
    """Конвертує список слотів у текст для користувача"""
    text = "Ось доступні слоти для запису:\n\n"
    for i, (start, _) in enumerate(slots[:limit]):
        formatted = format_datetime_for_user(start)
        text += f"{i+1}. {formatted}\n"
    return text.strip()

def is_valid_slot_choice(choice: str, slots: list) -> bool:
    """Перевіряє, чи вибраний номер слота коректний"""
    if not choice.isdigit():
        return False
    idx = int(choice) - 1
    return 0 <= idx < len(slots)
