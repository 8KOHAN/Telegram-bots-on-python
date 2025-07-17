import asyncio
import subprocess

def messages_to_prompt(messages: list[dict]) -> str:
    prompt = ""
    for m in messages:
        role = m.get("role", "")
        content = m.get("content", "")
        prompt += f"{role}: {content}\n"
    prompt += "assistant:"
    return prompt

async def ask_llm(messages: list[dict]) -> str:
    prompt = messages_to_prompt(messages)
    try:
        result = await asyncio.to_thread(
            lambda: subprocess.run(
                ['ollama', 'run', 'gemma:7b'],
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
