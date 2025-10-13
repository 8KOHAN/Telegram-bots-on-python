from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.products import product_buttons, PRODUCTS
from handlers.keyboards.inline_kp import category_buttons

router = Router()

@router.callback_query(F.data.startswith("category:"))
async def handle_category(callback: CallbackQuery):
    category = callback.data.split(":")[1]
    await callback.message.delete()

    filtered_products = {key: value for key, value in PRODUCTS.items() if key.startswith(category)}

    if filtered_products:
        kb = product_buttons(category, filtered_products)
        await callback.message.answer("Select a product:", reply_markup=kb)
    else:
        empty_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back:categories")]
        ])
        await callback.message.answer("There are no products available in this category", reply_markup=empty_kb)

@router.callback_query(F.data.startswith("product:"))
async def handle_product(callback: CallbackQuery):
    product_id = callback.data.split(":", 1)[1]
    product = PRODUCTS.get(product_id)

    await callback.message.delete()

    if product:
        text = (
            f"<b>{product['name']}</b>\n\n"
            f"{product['desc']}\n\n"
            f"<b>Price:</b> {product['price']} $"
        )
        buttons = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🛒 Buy", callback_data="buy"),
            InlineKeyboardButton(text="🔙 Back", callback_data=f"back:products:{product_id.split('_')[0]}")
        ]])
        await callback.message.answer_photo(
            photo=product["image"],
            caption=text,
            reply_markup=buttons,
            parse_mode="HTML"
        )
    else:
        await callback.message.answer("Product not found")

@router.callback_query(F.data.startswith("back:"))
async def handle_back(callback: CallbackQuery):
    parts = callback.data.split(":")
    where = parts[1]

    await callback.message.delete()

    if where == "categories":
        await callback.message.answer("Select a category:", reply_markup=category_buttons())
    elif where == "products":
        category = parts[2]
        filtered_products = {key: value for key, value in PRODUCTS.items() if key.startswith(category)}
        if filtered_products:
            await callback.message.answer("Select a product:", reply_markup=product_buttons(category, filtered_products))
        else:
            await callback.message.answer("There are no products available in this category")

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    await callback.message.edit_text("Select a category:", reply_markup=category_buttons())

@router.callback_query(F.data.startswith("view_"))
async def view_product(callback: CallbackQuery):
    pid = callback.data.replace("view_", "")
    product = PRODUCTS.get(pid)

    if not product:
        await callback.answer("Product not found")
        return

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=product["image"],
        caption=f"📦 {product['name']}\n\n📝 {product['desc']}\n💰 Price: {product['price']} $",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data=f"back:products:{pid.split('_')[0]}")]
        ])
    )

@router.callback_query(F.data == "buy")
async def handle_buy(callback: CallbackQuery):
    await callback.answer("✅ Your order has been placed! We will contact you", show_alert=True)
