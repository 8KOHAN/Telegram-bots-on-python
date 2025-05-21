from contextlib import suppress
from asyncio import sleep
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.factories import AdminFactory
from bot.core.database import Database
from bot.core.entities import Channel


router = Router()


def _menu_text(channel: Channel) -> str:

    return (
        "<b>меню канала</b>🧑🏻‍💼\n\n"
        f"<b>{channel.full_name}\n"
        f"id: {channel.channel_id}\n"        
        f"{'@' + channel.username if channel.username else ''}</b>\n\n"
    )


@router.callback_query(AdminFactory.filter(F.action == "channels"))
async def process_callback_query(
        callback_query: CallbackQuery,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # make channels text
    channels = await Channel.all_from_database(database=database_)

    text = "<b>оберіть канал який ви хочете переглянути</b>📣\n\n"
    channels_list = []

    for channel in channels:
        text += (
            f"<b>{channel.full_name}\n"
            f"id: {channel.channel_id}\n"
            f"{'@' + channel.username if channel.username else ''}</b>\n\n"
        )
        channels_list.append([channel.full_name, str(channel.channel_id)])
    
    # send message
    await callback_query.message.answer(
        text=text,
        reply_markup=AdminFactory.menu.choose_channel(channels=channels_list)
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "channel_settings"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get admin
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)

    # send message
    await callback_query.message.answer(
        text=_menu_text(channel=channel),
        reply_markup=AdminFactory.menu.channel(channel_id=callback_data.value)
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "accept_req"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        bot: Bot,
        database_: Database,
):

    # try to get chat
    try:
        chat = await bot.get_chat(chat_id=int(callback_data.value))
    except:
        await callback_query.message.answer(
            text="<b>помилка, перевірте айді каналу або перевірте чи є бот адміністратором каналу</b> ⚠️",
        )
        return

    # get join requests
    all_requests = await JoinRequest.all_from_database_by(channel_id=int(callback_data.value), database=database_)

    await callback_query.message.answer(
        text=f"<b>буде прийнято {len(all_requests)} запитів в канал {chat.full_name}</b> ℹ️",
    )

    # close callback
    await callback_query.answer()

    all_accepted = 0
    used_links = {}

    for join_request in all_requests:
        await sleep(0.3)
        try:
            await bot.approve_chat_join_request(
                chat_id=join_request.channel_id,
                user_id=join_request.user_id
            )
        except:
            pass
        else:
            all_accepted += 1
            user = await User.from_database(user_id=join_request.user_id, database=database_)
            user.link = join_request.link
            await user.commit()
            if join_request.link not in used_links.keys():
                used_links[join_request.link] = 1
            else:
                used_links[join_request.link] += 1
        finally:
            await join_request.delete()

    # add links statistic
    for link in used_links:
        channel_link = await ChannelLink.from_database(link=link, database=database_)
        channel_link.total_users += used_links[link]
        await channel_link.commit()

    await callback_query.message.answer(
        text=f"<b>прийнято {all_accepted} запитів в канал {chat.full_name}</b> ℹ️",
    )


@router.callback_query(AdminFactory.filter(F.action == "add_channel"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        bot: Bot,
        database_: Database,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # try to get chat
    try:
        chat = await bot.get_chat(chat_id=int(callback_data.value))
    except:
        await callback_query.message.answer(
            text="<b>помилка, перевірте айді каналу або перевірте чи є бот адміністратором каналу</b> ⚠️",
            reply_markup=AdminFactory.back(),
        )
        return
    # create channel
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)

    channel.username = chat.username
    channel.full_name = chat.full_name
    await channel.commit()

    await callback_query.message.answer(
        text=f"<b>канал {chat.full_name} створено</b> ℹ️",
        reply_markup=AdminFactory.back(),
    )
    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "set_auto_a_t"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # update channel
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)
    channel.auto_accept = True
    await channel.commit()

    # send message
    await callback_query.message.answer(
        text=_menu_text(channel=channel),
        reply_markup=AdminFactory.menu.channel(channel_id=callback_data.value)
    )
    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "set_auto_a_f"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # update channel
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)
    channel.auto_accept = False
    await channel.commit()

    # send message
    await callback_query.message.answer(
        text=_menu_text(channel=channel),
        reply_markup=AdminFactory.menu.channel(channel_id=callback_data.value)
    )
    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "delete_channel"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        bot: Bot,
        database_: Database,
):
    # clear message
    with suppress(Exception):
        await callback_query.message.delete()

    # delete channel
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)
    await channel.delete()

    with suppress(Exception):
        await bot.leave_chat(chat_id=int(callback_data.value))

    await callback_query.message.answer(
        text=f"<b>канал {channel.full_name} видалено</b> ℹ️",
        reply_markup=AdminFactory.back(),
    )

    # close callback
    await callback_query.answer()
