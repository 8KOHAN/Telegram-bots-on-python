from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.factories import AdminFactory
from bot.core.entities import Admin

router = Router()


@router.message(Command(commands=['start', 'menu']))
async def process_message(
        message: Message,
        admin_: Admin
):
        await message.answer(
            text="<b>ви в меню</b> 📝\n\n"
                 "оберіть пункти які вас цікавлять",
            reply_markup=AdminFactory.menu.main()
        )


@router.callback_query(F.data == "menu")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # clear state
    await state.clear()

    # send message
    await callback_query.message.answer(
        text="<b>ви в меню</b> 📝\n\n"
             "оберіть пункти які вас цікавлять",
        reply_markup=AdminFactory.menu.main()
    )

    # close callback
    await callback_query.answer()
