from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from handlers.fsm_states import AddProduct
from handlers.keyboards.admin_kp import admin_main_kb, admin_category_kb, add_category_kb, product_list_kb
from data.products import PRODUCTS, save_products, product_buttons

router = Router()
ADMIN_IDS = [0000000000, 0000000000] # Tlegramm ID user

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("🔧 Админ-панель", reply_markup=admin_main_kb())
    else:
        await message.answer("⛔ У тебя нет доступа!")

@router.callback_query(F.data == "back_admin_main")
async def admin_access(callback: CallbackQuery):
    if callback.from_user.id in ADMIN_IDS:
        await callback.message.edit_text("🔧 Админ-панель", reply_markup=admin_main_kb())
        await callback.answer()

@router.callback_query(F.data == "admin_add")
async def add_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выбери категорию:", reply_markup=add_category_kb())
    await state.set_state(AddProduct.choosing_category)

@router.message(AddProduct.entering_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📝 Введи описание товара:")
    await state.set_state(AddProduct.entering_desc)

@router.message(AddProduct.entering_desc)
async def enter_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("💲 Введи цену товара:")
    await state.set_state(AddProduct.entering_price)

@router.message(AddProduct.entering_price)
async def enter_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("📷 Отправь фото товара:")
    await state.set_state(AddProduct.uploading_photo)

@router.message(AddProduct.uploading_photo)
async def upload_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❗ Отправь именно фото.")
        return

    photo_id = message.photo[-1].file_id
    data = await state.get_data()

    product_id = f"{data['category']}_{len(PRODUCTS)}"
    PRODUCTS[product_id] = {
        "name": data['name'],
        "desc": data['desc'],
        "price": data['price'],
        "image": photo_id
    }
    save_products()

    await message.answer(f"✅ Товар добавлен: {data['name']}")
    await state.clear()

@router.callback_query(F.data.startswith("del_"))
async def delete_product(callback: CallbackQuery):
    pid = callback.data.split("_", 1)[1]
    if pid in PRODUCTS:
        del PRODUCTS[pid]
        save_products()
        await callback.message.edit_text("✅ Товар удалён.")
    else:
        await callback.answer("❌ Товар не найден.")

@router.callback_query(F.data == "admin_cat")
async def open_admin_categories(callback: CallbackQuery):
    await callback.message.edit_text("Выбери категорию:", reply_markup=admin_category_kb())


@router.callback_query(F.data == "back_admin_categories")
async def back_admin_categories(callback: CallbackQuery):
    await callback.message.edit_text("Выбери категорию:", reply_markup=admin_category_kb())

@router.callback_query(F.data.startswith("admin_cat_manage_"))
async def admin_manage_category(callback: CallbackQuery):
    category = callback.data.split("_")[-1]

    items = {
        pid: p for pid, p in PRODUCTS.items()
        if pid.startswith(category)
    }

    if not items:
        await callback.message.edit_text("⚠️ Нет товаров в этой категории.", reply_markup=admin_category_kb())
        return

    kb = product_list_kb(category, PRODUCTS)
    await callback.message.edit_text("🗑 Выберите товар для удаления:", reply_markup=kb)

@router.callback_query(F.data.startswith("admin_add_cat_"))
async def choose_category_for_adding(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[-1]
    await state.update_data(category=category)
    await callback.message.answer("✏️ Введи название товара:")
    await state.set_state(AddProduct.entering_name)
