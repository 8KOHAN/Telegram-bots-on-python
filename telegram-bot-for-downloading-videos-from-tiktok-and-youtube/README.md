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

## Project Structure

```bash
telegram-downloader-bot/
├── bot.py                  
├── url_storage.py          
├── handlers/
│   ├── callback.py         
│   ├── commands.py         
│   ├── function.py         
│   └── keyboards/
│       └── inline_kp.py    
├── downloads/              
├── url_storage.json        
└── .env                    
```
