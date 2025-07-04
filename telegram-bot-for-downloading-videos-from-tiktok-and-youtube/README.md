# Telegram Video & Audio Downloader Bot

A powerful and easy-to-use Telegram bot that allows users to download **videos and audio from TikTok and YouTube** directly via chat.

> Built with `aiogram` and `yt-dlp` for fast and reliable performance.

---

## Features

- Supports TikTok, YouTube, and YouTube Shorts URLs
- Choose between **video or audio** download formats
- Auto-creates a `downloads/` folder and manages file cleanup
- Stores URL history using a JSON file

---

## Getting Started

```bash
Project Structure

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
```
Notes

- All files are automatically deleted after sending to the user.
- Designed for personal or small-scale use.
- espect the terms of service of TikTok and YouTube when using this bot.
