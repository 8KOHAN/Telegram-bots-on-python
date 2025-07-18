import asyncio
import subprocess
import os

# Використовуємо модель з конфігурації або дефолт
LLM_MODEL = os.getenv("LLM_MODEL", "gemma:7b")


def messages_to_prompt(messages: list[dict]) -> str:
    """
    Формуємо prompt у вигляді:
    system: <content>\n
    user: <content>\n
    assistant:
    """
    prompt_lines = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        prompt_lines.append(f"{role}: {content}")
    # Додаємо маркер початку відповіді асистента
    prompt_lines.append("assistant:")
    return "\n".join(prompt_lines) + "\n"


async def ask_llm(messages: list[dict]) -> str:
    """
    Викликаємо локальну модель через ollama.
    Передаємо сформований prompt на stdin процесу.
    """
    prompt = messages_to_prompt(messages)
    # Логування для дебагу
    print("[DEBUG] Prompt sent to LLM:\n", prompt)
    try:
        # Запускаємо у фоновому потоці
        result = await asyncio.to_thread(
            lambda: subprocess.run(
                ["ollama", "run", LLM_MODEL],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
        )
        # Повертаємо stdout без зайвих пробілів
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Ollama subprocess error: {e}")
        print(f"stderr: {e.stderr}")
        print(f"stdout: {e.stdout}")
        return "Вибачте, сталася помилка під час відповіді від AI."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Вибачте, сталася помилка під час відповіді від AI."
