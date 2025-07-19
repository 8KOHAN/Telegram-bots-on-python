from aiogram import Router, types
from services.llm_client import ask_llm
from utils.text_utils import normalize_text

router = Router()

with open("bot/prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT_FULL = f.read()

@router.message()
async def handle_user_message(message: types.Message):
    user_text = normalize_text(message.text)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_FULL},
        {"role": "user", "content": user_text}
    ]

    print(f"[DEBUG] Prompt messages: {messages}")
    reply_text = await ask_llm(messages)

    await message.answer(reply_text)
