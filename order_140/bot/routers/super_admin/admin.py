from contextlib import suppress
from typing import Tuple

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.factories import AdminFactory
from bot.fsm.states import SuperAdminStates
from bot.core.database import Database
from bot.core.entities import Admin

router = Router()


def _menu_text(admin: Admin) -> str:
    return (
        "<b>меню адміністратора</b>🧑🏻‍💼\n\n"
        f"<b><a href='tg://user?id={admin.user_id}'>{admin.full_name}</a> {'@' + admin.username if admin.username else ''}</b>\n"
        f"id: <code>{admin.user_id}</code>\n"
    )


@router.callback_query(AdminFactory.filter(F.action == "admins"))
async def process_callback_query(
        callback_query: CallbackQuery,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    admins = await Admin.all_from_database(database=database_)

    # make admins text and list
    text = "<b>оберіть адміністратора якого ви хочете переглянути</b>🧑🏻‍💼\n\n"
    admins_list = []

    for admin in admins:
        text += (
            f"<b><a href='tg://user?id={admin.user_id}'>{admin.full_name}</a> {'@' + admin.username if admin.username else ''}</b>\n"
            f"id: <code>{admin.user_id}</code>\n"
        )
        admins_list.append([admin.full_name, str(admin.user_id)])

    # send message
    await callback_query.message.answer(
        text=text,
        reply_markup=AdminFactory.menu.choose_admin(admins=admins_list)
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "admin_settings"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get admin
    admin = await Admin.from_database(user_id=int(callback_data.value), database=database_)

    # send message
    await callback_query.message.answer(
        text=_menu_text(admin=admin),
        reply_markup=AdminFactory.menu.admin(admin_id=callback_data.value)
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "set_adm_sup"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # delete admin
    admin = await Admin.from_database(user_id=int(callback_data.value), database=database_)
    await admin.commit()

    # send message
    await callback_query.message.answer(
        text=_menu_text(admin=admin),
        reply_markup=AdminFactory.menu.admin(admin_id=callback_data.value)
    )
    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "set_adm_n_sup"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # delete admin
    admin = await Admin.from_database(user_id=int(callback_data.value), database=database_)
    await admin.commit()

    # send message
    await callback_query.message.answer(
        text=_menu_text(admin=admin),
        reply_markup=AdminFactory.menu.admin(admin_id=callback_data.value)
    )
    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "add_admin"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # send message
    await callback_query.message.answer(
        text="<b>введіть айді адміну якого ви хочете додати</b> ℹ️",       #разобраться с этимм
        reply_markup=AdminFactory.back()
    )


@router.message(StateFilter(SuperAdminStates.add_admin_enter_id))
async def process_message(
        message: Message,
        state: FSMContext,
        bot: Bot,
        database_: Database,
):
    # clear message
    with suppress(Exception):
        await message.delete()

    # try to get chat
    try:
        chat = await bot.get_chat(chat_id=int(message.text))
    except:
        await message.answer(
            text="<b>помилка,перевірте чи є у користувача чат з ботом каналу</b> ⚠️",
            reply_markup=AdminFactory.back(),
        )
        return

    # get data

    # create admin
    admin = await Admin.create(user_id=int(message.text), database=database_)

    # update data
    admin.username = chat.username
    admin.full_name = chat.full_name
    await admin.commit()

    await message.answer(
        text=f"<b>адміна {chat.full_name} додано</b> ℹ️",
        reply_markup=AdminFactory.back(),
    )

    await state.clear()


@router.callback_query(AdminFactory.filter(F.action == "delete_admin"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # delete admin
    admin = await Admin.from_database(user_id=int(callback_data.value), database=database_)
    await admin.delete()

    await callback_query.message.answer(
        text=f"<b>адміна {admin.full_name} видалено</b> ℹ️",
        reply_markup=AdminFactory.back(),
    )
    # close callback
    await callback_query.answer()
