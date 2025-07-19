# Telegram Online Store Bot

A sleek and practical **Telegram store bot** for browsing and purchasing **phones and PCs**. Offers an intuitive shopping flow for users, and a secure admin panel for managing the product catalog — all stored in a local JSON file.

> Powered by `aiogram`, with a smooth UI and persistent storage.

---

## User Features

- Browse a catalog of **phones and PCs**
- View detailed product cards with images and descriptions
- Universal **Back button** — re-sends the previous message and deletes the old one
- Choose what to buy via inline buttons
- Use `/start` and `/help` for simple guidance

---

## Admin Panel

> Only accessible to users **hardcoded in the bot**

- Add new products (name, price, image, description)
- Remove products easily
- Full **Back button** support in admin interface
- **All products are saved in a `products.json` file** — no database required

---

## Persistent Storage

- All products are saved and loaded from `data/products.json`
- Automatically updated when products are added or removed
- No need for external databases or setup

---

## Project Structure

```bash
├── bot.py
├── data/
│   └── products.py
├── handlers/
│   ├── admin.py
│   ├── callback.py
│   ├── commands.py
│   ├── fsm_states.py
│   └── keyboards/
│       ├── admin_kb.py  
│       ├── reply_kp.py
│       ├── inline_kb.py
```
