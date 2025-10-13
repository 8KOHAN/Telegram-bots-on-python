from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add product", callback_data="admin_add")],
        [InlineKeyboardButton(text="📂 Categories", callback_data="admin_cat")]
    ])

def admin_category_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥 Computers", callback_data="admin_cat_manage_computers")],
        [InlineKeyboardButton(text="📱 Phones", callback_data="admin_cat_manage_phones")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_admin_main")]
    ])

def add_category_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖥 Computers", callback_data="admin_add_cat_computers")],
        [InlineKeyboardButton(text="📱 Phones", callback_data="admin_add_cat_phones")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_admin_main")]
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
        InlineKeyboardButton(text="◀️ Back", callback_data="back_admin_categories")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons or [[InlineKeyboardButton(text="(empty)", callback_data="none")]])
