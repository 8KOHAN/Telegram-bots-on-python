from aiogram import Router, types
from aiogram.filters import CommandStart
from datetime import datetime, timedelta

from services.llm_client import ask_llm
from services.calendar import list_free_slots, create_appointment
from services.dialog_state import add_to_history, dialog_history
from utils.formatting import format_datetime_for_user
from utils.slot_parser import slots_to_text
from utils.text_utils import normalize_text

router = Router()

with open("bot/prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

@router.message()
async def handle_user_message(message: types.Message):
    user_id = message.from_user.id
    user_text = normalize_text(message.text)

    # Якщо користувач вводить номер слота
    if user_text.isdigit():
        idx = int(user_text) - 1
        history = dialog_history.get(user_id, [])
        for entry in history:
            if entry["role"] == "system" and entry["content"].startswith("slots:"):
                try:
                    slots = eval(entry["content"][6:])
                    if 0 <= idx < len(slots):
                        start_iso, end_iso = slots[idx]
                        create_appointment(
                            start_iso=start_iso,
                            end_iso=end_iso,
                            summary="Лазерна епіляція",
                            description=f"Запис через Telegram (ID {user_id})"
                        )
                        formatted_time = format_datetime_for_user(start_iso)
                        await message.answer(f"Запис підтверджено ✅ Чекаємо вас {formatted_time}")
                        return
                    else:
                        await message.answer("Будь ласка, оберіть номер зі списку 📋")
                        return
                except Exception as e:
                    print(f"[SLOT SELECT ERROR] {e}")
                    await message.answer("Вибачте, сталася помилка при записі 😔")
                    return

    # Підготовка prompt для локальної LLM
    add_to_history(user_id, "user", message.text)
    history = dialog_history.get(user_id, [])
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    reply = await ask_llm(messages)
    add_to_history(user_id, "assistant", reply)
    await message.answer(reply)

    # Якщо GPT сказав "Зараз підберу для вас доступні слоти..."
    if "зараз підберу для вас доступні слоти" in reply.lower():
        now = datetime.utcnow()
        try:
            slots = list_free_slots(
                start_iso=now.isoformat(),
                end_iso=(now + timedelta(days=3)).isoformat(),
                duration_minutes=30
            )
            if not slots:
                await message.answer("На жаль, наразі немає вільних слотів. Напишіть, будь ласка, пізніше 🙏")
                return

            text = slots_to_text(slots)

            add_to_history(user_id, "system", "slots:" + str(slots))
            await message.answer(text + "\nНапишіть номер слота, який вам підходить 👇")
        except Exception as e:
            print(f"[SLOT FETCH ERROR] {e}")
            await message.answer("Не вдалося отримати список слотів 😓")
