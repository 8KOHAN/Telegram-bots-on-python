import json
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PRODUCTS_FILE = "data/products.json"
PRODUCTS = {}

def load_products():
    global PRODUCTS
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            PRODUCTS = json.load(f)
    else:
        PRODUCTS = {}

def save_products():
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(PRODUCTS, f, ensure_ascii=False, indent=2)

load_products()

def product_buttons(category, products: dict):
    product_buttons_list = [
        InlineKeyboardButton(text=prod["name"], callback_data=f"product:{key}")
        for key, prod in products.items()
        if key.startswith(category)
    ]

    keyboard_rows = [[button] for button in product_buttons_list]

    keyboard_rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:categories")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
