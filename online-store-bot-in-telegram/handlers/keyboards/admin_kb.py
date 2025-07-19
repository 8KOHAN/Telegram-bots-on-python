from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add")],
        [InlineKeyboardButton(text="📂 Категории", callback_data="admin_cat")]
    ])

def admin_category_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥 Компьютеры", callback_data="admin_cat_manage_computers")],
        [InlineKeyboardButton(text="📱 Телефоны", callback_data="admin_cat_manage_phones")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_admin_main")]
    ])

def add_category_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥 Компьютеры", callback_data="admin_add_cat_computers")],
        [InlineKeyboardButton(text="📱 Телефоны", callback_data="admin_add_cat_phones")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_admin_main")]
    ])

def product_list_kb(category: str, products: dict):
    buttons = []
    for pid, info in products.items():
        if pid.startswith(category):
            buttons.append([
                InlineKeyboardButton(
                    text=f"❌ {info['name']}",
                    callback_data=f"del_{pid}"
                )
            ])
    buttons.append([
        InlineKeyboardButton(text="◀️ Назад", callback_data="back_admin_categories")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons or [[InlineKeyboardButton(text="(пусто)", callback_data="none")]])
