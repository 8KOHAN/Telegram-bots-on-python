# 🎬 Telegram Video & Audio Downloader Bot

A powerful and easy-to-use Telegram bot that allows users to download **videos and audio from TikTok and YouTube** directly via chat.

> Built with `aiogram` and `yt-dlp` for fast and reliable performance.

---

## ⚡ Features

- ✅ Supports TikTok, YouTube, and YouTube Shorts URLs
- 🎵 Choose between **video or audio** download formats
- 📂 Auto-creates a `downloads/` folder and manages file cleanup
- 💾 Stores URL history using a simple JSON file

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-downloader-bot.git
cd telegram-downloader-bot

2. Install dependencies

pip install -r requirements.txt

3. Add your bot token

Create a .env file in the root directory and paste:

BOT_TOKEN=your_telegram_bot_token_here

4. Run the bot

python bot.py

📁 Project Structure

telegram-downloader-bot/
├── bot.py                    # Entry point
├── url_storage.py            # Handles URL storage
├── handlers/
│   ├── callback.py           # Handles inline button callbacks
│   ├── commands.py           # /start and URL message handlers
│   ├── function.py           # Video/audio download logic
│   └── keyboards/
│       └── inline_kp.py      # Inline keyboard buttons
├── downloads/                # Downloaded files (auto-created)
├── url_storage.json          # Stored URLs
└── .env                      # Your bot token (not committed)

📌 Notes

    All files are automatically deleted after sending to the user.

    Designed for personal or small-scale use.

    Respect the terms of service of TikTok and YouTube when using this bot.
