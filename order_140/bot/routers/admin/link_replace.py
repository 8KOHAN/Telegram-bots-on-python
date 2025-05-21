from contextlib import suppress
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.fsm.states import AdminStates
from bot.keyboards.factories import AdminFactory
import re

router = Router()


@router.callback_query(AdminFactory.filter(F.action == "replace_link"))
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    await callback_query.message.answer(
        text="перешлiть пост для замiни посилання",
        reply_markup=AdminFactory.back()
    )
    await state.set_state(AdminStates.forward_post)
    await callback_query.answer()


@router.message(AdminStates.forward_post)
async def process_message(
        message: Message,
        state: FSMContext
):
    await state.set_data(dict(text=str(message.html_text), markup=message.reply_markup if message.reply_markup else 0, photo=message.photo[-1].file_id if message.photo else 0))
    await message.answer("введiть посилання на яке бажаєте замiнити")
    await state.set_state(AdminStates.enter_replace_link)


@router.message(AdminStates.enter_replace_link)
async def process_message(
        message: Message,
        state: FSMContext
):
    text = (await state.get_data())["text"]
    photo = (await state.get_data())["photo"]
    markup = (await state.get_data())["markup"]
    link_pattern = r'("https?://\S+")'

    link = '"' + message.text + '"'
    new_text = re.sub(link_pattern, link, text)

    if photo == 0:
        if markup == 0:
            await message.answer(
                text=new_text,
            )

        else:
            await message.answer(
                text=new_text,
                reply_markup=AdminFactory.new_reply_markup(markup=markup, link=link.replace('"', ''))
            )
        #with photo
    else:
        if markup == 0:
            await message.answer_photo(
                photo=photo,
                caption=new_text,
            )

        else:
            await message.answer_photo(
                photo=photo,
                caption=new_text,
                reply_markup=AdminFactory.new_reply_markup(markup=markup, link=link.replace('"', ''))
            )

    await message.answer(
        text="Посилання замiненi",
        reply_markup=AdminFactory.back()
    )
    await state.clear()
