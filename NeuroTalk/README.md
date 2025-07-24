# NeuroTalk — AI Manager in Telegram

**NeuroTalk** is a Telegram bot for a laser epilation specialist that chats with clients, answers questions, and helps book procedures via Google Calendar.

---

## AI Manager
- Communicates in Ukrainian.
- Automatically handles frequently asked questions (FAQ).
- Responds to common objections: "Does it hurt?", "Too expensive", "From what age?" and more.
- Simulates realistic communication on behalf of the specialist.

---

## Technologies

- `Python 3.10+`
- `Aiogram` 
- `gemma:7b` (LLM)

---

## Project Structure

```bash
bot/
├── handlers/
│   ├── base.py
│   ├── booking.py
│   └── start.py
├── keyboards/                       
│   └── reply.py            
├── prompts/
│   └── system_prompt.txt
├── services/
│   └── llm_client.py
├── utils/
│   └── text_utils.py
├── config.py
└── main.py
.env
requirements.txt
```
