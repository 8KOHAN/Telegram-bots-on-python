# 🛍️ Telegram Online Store Bot

A sleek and practical **Telegram store bot** for browsing and purchasing **phones and PCs**. Offers an intuitive shopping flow for users, and a secure admin panel for managing the product catalog — all stored in a local JSON file.

> Powered by `aiogram`, with a smooth UI and persistent storage.

---

## 👤 User Features

- 📱 Browse a catalog of **phones and PCs**
- 📷 View detailed product cards with images and descriptions
- ↩️ Universal **Back button** — re-sends the previous message and deletes the old one
- 🛒 Choose what to buy via inline buttons
- ❓ Use `/start` and `/help` for simple guidance

---

## 🔐 Admin Panel

> Only accessible to users **hardcoded in the bot**

- ➕ Add new products (name, price, image, description)
- 🗑️ Remove products easily
- ↩️ Full **Back button** support in admin interface
- 💾 **All products are saved in a `products.json` file** — no database required

---

## 🗃️ Persistent Storage

- All products are saved and loaded from `data/products.json`
- Automatically updated when products are added or removed
- No need for external databases or setup

---

## 🛠️ Project Structure

```bash
online-store-bot-in-telegram/
├── bot.py # Entry point
├── data/
│ └── products.py # Manages product data (JSON storage)
├── handlers/
│ ├── admin.py # Admin interface (add/delete products)
│ ├── callback.py # User navigation and selection
│ ├── commands.py # /start and /help handlers
│ └── fsm_states.py # FSM states for admin flows
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/online-store-bot-in-telegram.git
cd online-store-bot-in-telegram

2. Install dependencies

pip install -r requirements.txt

3. Add your bot token

Create a .env file:

BOT_TOKEN=your_telegram_token

4. Run the bot

python bot.py

📦 Tech Stack

    Python

    aiogram

    yt-dlp (optional if you expand with video previews)

    JSON storage (no database needed)

👀 Example Usage

    Type /start to browse the catalog

    Select a product → view details

    Not interested? Tap ↩️ Back

    Admins: manage products through simple UI with protected access

