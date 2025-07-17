def normalize_text(text: str) -> str:
    """Нормалізує текст (нижній регістр, без зайвих пробілів)"""
    return text.strip().lower()

def contains_keywords(text: str, keywords: list[str]) -> bool:
    """Перевіряє, чи текст містить хоча б одне ключове слово"""
    text = normalize_text(text)
    return any(keyword.lower() in text for keyword in keywords)
