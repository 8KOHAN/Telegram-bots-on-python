from contextlib import suppress
from aiogram import Router, F, Bot
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

from bot.keyboards.factories import AdminFactory
from bot.core.database import Database
from bot.core.entities import Admin


router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def process_my_chat_member(
        my_chat_member: ChatMemberUpdated,
        bot: Bot,
        database_: Database
):
    # get admins
    admins = await Admin.all_from_database(database=database_)

    # send message to super admins
    for admin in admins:
        with suppress(Exception):
            await bot.send_message(
                chat_id=admin.user_id,
                text="<b>бота було додано в канал ℹ️</b>\n\n"
                     f"{my_chat_member.chat.full_name}\n"
                     f"{my_chat_member.chat.id}\n"
                     f"{my_chat_member.chat.username if my_chat_member.chat.username else ''}\n"
                     f"<b>додати канал в базу данних ?</b>",
                reply_markup=AdminFactory.add_channel(channel_id=str(my_chat_member.chat.id))
            )

