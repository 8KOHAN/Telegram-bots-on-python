import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "gemma:7b")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_CALENDAR_HTTPS = os.getenv("GOOGLE_CALENDAR_HTTPS")
