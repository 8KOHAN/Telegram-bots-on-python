import asyncio
import subprocess
import os

LLM_MODEL = os.getenv("LLM_MODEL", "gemma:7b")


def messages_to_prompt(messages: list[dict]) -> str:
    prompt_lines = []
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        prompt_lines.append(f"{role}: {content}")
    prompt_lines.append("assistant:")
    return "\n".join(prompt_lines) + "\n"


async def ask_llm(messages: list[dict]) -> str:
    prompt = messages_to_prompt(messages)
    print("[DEBUG] Prompt sent to LLM:\n", prompt)
    try:
        result = await asyncio.to_thread(
            lambda: subprocess.run(
                ["ollama", "run", LLM_MODEL],
                input=prompt,
                text=True,
                capture_output=True,
                check=True
            )
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Ollama subprocess error: {e}")
        print(f"stderr: {e.stderr}")
        print(f"stdout: {e.stdout}")
        return "Вибачте, сталася помилка під час відповіді від AI."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Вибачте, сталася помилка під час відповіді від AI."
