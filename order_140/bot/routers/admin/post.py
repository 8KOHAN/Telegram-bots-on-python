from contextlib import suppress
from datetime import datetime, timedelta
from importlib.metadata import Lookup

from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, PhotoSize
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import asyncio
from aiogram_album import AlbumMessage
from telethon.tl.types.photos import Photo

from bot.fsm.states import AdminStates
from bot.keyboards.factories import AdminFactory, AdminFactory

from bot.core.database import Database
from bot.core.entities import Channel, Admin, Post
from bot.core.configuration import Configuration
from bot.fsm.fsm_func import MassSendStates

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

def send_ads_post():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            {"text": "Так", "callback_data": "send_post"},
            {"text": "Ні", "callback_data": "cancel_post"}
        ]
    ])
    return keyboard

# Функція для створення кнопок
def create_button_post(buttons):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for button in buttons:
        for text, url in button.items():
            keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard

@router.callback_query(F.data == "add_buttons")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await callback_query.message.answer(
        text="Відбрав кнопки у форматі: \n\n<code>текст::посилання$$текст::посилання</code> - рядок\n<code>текст::посилання</code>\n\nЯкщо треба без кнопок: <code>-</code>\n\nВідмінити дію - /admin"
    )
    await state.set_state(MassSendStates.buttons)

@router.message(MassSendStates.buttons)
async def process_handler(
        message: Message,
        state: FSMContext,
        bot: Bot,
):
    await message.delete()
    all_buttons = []
    state_data = await state.get_data()
    kb_send = send_ads_post()  # Функція для створення клавіатури для відправки поста

    if message.text == "-":
        await message.answer(
            text="Розіслати цей пост?",
            reply_markup=kb_send
        )
        return

    try:
        for i in message.text.split("\n"):
            line = i.split("$$")
            dct = {}
            for j in line:
                text, url = j.split("::")
                dct[text] = url.strip()
            all_buttons.append(dct)
    except Exception as e:
        wrong = await message.answer("Помилка: " + str(e))
        await asyncio.sleep(3)
        await wrong.delete()
    else:
        create_buttons = create_button_post(all_buttons)  # Функція для створення кнопок
        if create_buttons:
            working_message = state_data["working_message"]
            state_data["inline_kb"] = all_buttons
            await bot.edit_message_reply_markup(
                chat_id=message.from_user.id,
                message_id=working_message.message_id,
                reply_markup=create_buttons,
            )
            await state.set_data(state_data)
            await message.answer(
                text="Розіслати цей пост?",
                reply_markup=kb_send
            )
        else:
            await message.answer("Невірний формат кнопок")
    await state.clear()

@router.callback_query(F.data == "change_description")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
        database_: Database,
):
    await callback_query.message.answer("Відправте новий опис поста.")
    await state.set_state(AdminStates.change_description)

@router.message(StateFilter(AdminStates.change_description))
async def process_message(
        message: Message,
        state: FSMContext,
        database_: Database,
        bot: Bot
):
    state_data = await state.get_data()
    post = state_data.get("post")

    if post:
        post.content = message.html_text  # Змінюємо опис поста
        await post.commit()  # Зберігаємо зміни в базі даних
        await state.update_data(data=dict(post=post))

        # Відправляємо новий опис в меню
        await message.answer(
            text=f"Новий опис поста:\n{post.content}",
            reply_markup=AdminFactory.posts.post_settings()  # Показуємо меню з налаштуваннями поста
        )
    else:
        await message.answer("Не вдалося знайти пост для зміни опису.")


def _menu_text(channel: Channel) -> str:
    return (
        f"<b>меню поста 📝</b>\n\n"
        f"посилання: <a href='{...}'></a>\n"
        f"канал:\n"
        f"ім\'я каналу: {channel.full_name} 📣\n"
        f"{'  юзернейм каналу: @' + channel.username + '📣' if channel.username else ''}\n"
    )


def get_delay_until(target_time) -> int:
    print(target_time)
    now = datetime.now()
    delta = target_time - now
    # Если время уже прошло, возвращаем 0
    if delta.total_seconds() <= 0:
        return 0
    return int(delta.total_seconds())


async def forward_media(message: AlbumMessage, chat_id: int, target_time: str, sound: str, time_delete,
                        bot: Bot) -> list:
    delay = get_delay_until(target_time)
    await asyncio.sleep(delay)

    media_group = message.as_input_media(caption=message.html_text)
    msg = await bot.send_media_group(
        chat_id=chat_id,
        media=media_group,
        disable_notification=True if sound == "no" else False
    )
    for i in msg:
        print(i.message_id)
        await delete_message(chat_id=chat_id, message_id=i.message_id, target_time=time_delete, bot=bot)


async def forward_message(message: Message, chat_id: int, sound: str, bot: Bot, target_time=datetime.now(), time_delete=None) -> int:
    delay = get_delay_until(target_time)
    await asyncio.sleep(delay)

    if message.text:
        msg = await bot.send_message(
            text=message.html_text,
            chat_id=chat_id,
            disable_notification=True if sound == "no" else False
        )
    # photos, videos, animations
    elif message.caption:
        if message.photo:
            photo_id: str = message.photo[-1].file_id
            msg = await bot.send_photo(
                caption=message.html_text,
                chat_id=chat_id,
                disable_notification=True if sound == "no" else False,
                photo=photo_id,
                reply_markup=AdminFactory.posts.post_settings() if chat_id == message.from_user.id else None
            )
        elif message.video:
            video_id: str = message.video.file_id
            msg = await bot.send_video(
                caption=message.html_text,
                chat_id=chat_id,
                disable_notification=True if sound == "no" else False,
                video=video_id
            )
        elif message.animation:
            animation_id: str = message.animation.file_id
            msg = await bot.send_animation(
                caption=message.html_text,
                chat_id=chat_id,
                disable_notification=True if sound == "no" else False,
                animation=animation_id
            )
        for i in msg:
            print(i.message_id)
            await delete_message(chat_id=chat_id, message_id=i.message_id, target_time=time_delete, bot=bot)
        return msg[0].message_id


async def delete_message(chat_id: int, message_id: int, target_time: str, bot: Bot):
    delay = get_delay_until(target_time)
    # Задержка до удаления сообщения
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id, message_id)


@router.callback_query(AdminFactory.filter(F.action == "add_post"))
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
        database_: Database,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    channels = await Channel.all_from_database(database=database_)

    channels_list = []
    i = 0
    text = ""
    for channel in channels:
        i += 1
        text += f"{i} - <b>{channel.full_name}</b>"
        channels_list.append([channel.full_name, str(channel.channel_id)])

    await callback_query.message.answer(
        text=f'{text}\nНапишiть обранi номера каналiв⚡\nПриклад: <b>1,2,4,7</b>',
    )
    await state.set_state(AdminStates.choose_channel)

    await callback_query.answer()


@router.message(StateFilter(AdminStates.choose_channel))
async def process_message(
        message: Message,
        state: FSMContext,
):
    channel_nums = list(map(int, message.text.split(',')))

    await state.set_data(dict(channel_nums=channel_nums))

    await message.answer("<b>Увiмкнути коментарi?</b>", reply_markup=AdminFactory.posts.comments())
    await state.set_state(AdminStates.enter_link_name)


@router.callback_query(AdminFactory.filter(F.action == "comments"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    await state.update_data(comments=callback_data.value)
    await callback_query.message.answer("<b>Увiмкнути звук?</b>", reply_markup=AdminFactory.posts.sound())


@router.callback_query(AdminFactory.filter(F.action == "sound"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    await state.update_data(sound=callback_data.value)
    await callback_query.message.answer("<b>Коли запостити?</b>", reply_markup=AdminFactory.posts.time())


@router.callback_query(AdminFactory.filter(F.action == "time"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    if callback_data.value == "now":
        await state.update_data(time=callback_data.value)
        await callback_query.message.answer("Зробити автовидалення?", reply_markup=AdminFactory.posts.auto_delete())

    elif callback_data.value == "other":
        await callback_query.message.answer("<b>Напишiть дату та час вiдправки</b>\n"
                                            "Приклад: 15.09.2006 13:30")
        await state.set_state(AdminStates.print_time)


@router.message(StateFilter(AdminStates.print_time))
async def process_message(
        message: Message,
        state: FSMContext,
):
    try:
        post_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("<b>⚠️Неправильно написана дата.</b>\n"
                             "Приклад: 15.09.2006 13:30")
        return

    await state.update_data(time=post_time)
    await message.answer("Зробити автовидалення?", reply_markup=AdminFactory.posts.auto_delete())


@router.callback_query(AdminFactory.filter(F.action == "auto_delete"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    if callback_data.value == "yes":
        await callback_query.message.answer("<b>Напишiть дату та час видалення</b>\n"
                                            "Приклад: 15.09.2006 13:30")
        await state.set_state(AdminStates.print_time_delete)

    elif callback_data.value == "no":
        await state.update_data(time_delete=callback_data.value)
        await callback_query.message.answer("<b>Вiдправте пост</b>")
        await state.set_state(AdminStates.posting)


@router.message(StateFilter(AdminStates.print_time_delete))
async def process_message(
        message: Message,
        state: FSMContext,
):
    try:
        post_time_delete = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("<b>⚠️Неправильно написана дата.</b>\n"
                             "Приклад: 15.09.2006 13:30")
        return

    await state.update_data(time_delete=post_time_delete)
    await message.answer("<b>Вiдправте пост</b>")
    await state.set_state(AdminStates.posting)


@router.message(StateFilter(AdminStates.posting), F.media_group_id)
async def media_handler(
        message: AlbumMessage,
        bot: Bot,
        database_: Database,
        state: FSMContext
):
    channel_nums: list = (await state.get_data())["channel_nums"]
    sound: str = (await state.get_data())["sound"]
    time: str = (await state.get_data())["time"]
    time_delete: str = (await state.get_data())["time_delete"]

    channels = await Channel.all_from_database(database=database_)
    if time == "now":
        time = datetime.now()
    for num in channel_nums:
        await forward_media(
            chat_id=channels[num - 1].channel_id,
            target_time=time,
            sound=sound,
            bot=bot,
            message=message,
            time_delete=time_delete
        )


# @router.message(StateFilter(AdminStates.posting))
# async def process_message(
#         message: Message,
#         bot: Bot,
#         state: FSMContext,
#         database_: Database,
# ):
#     channel_nums: list = (await state.get_data())["channel_nums"]
#     sound: str = (await state.get_data())["sound"]
#     time: str = (await state.get_data())["time"]
#     time_delete: str = (await state.get_data())["time_delete"]
#
#     channels = await Channel.all_from_database(database=database_)
#     if time == "now":
#         time = datetime.now()
#     for num in channel_nums:
#         post_id = await forward_message(
#             chat_id=channels[num - 1].channel_id,
#             target_time=time,
#             sound=sound,
#             bot=bot,
#             message=message,
#             time_delete=time_delete
#         )
#         link = f"t.me/"
#         post = await Post.from_database(link=)


@router.callback_query(AdminFactory.filter(F.action == "refresh"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database,
):
    invite_link = "https://t.me/+" + callback_data.value

    link = await ChannelLink.from_database(link=invite_link, database=database_)
    reqs = await JoinRequest.all_from_database_by(link=link.link, database=database_)
    requests = len(reqs)

    try:
        await callback_query.message.edit_text(
            text=f"<b>посилання {link.name} успiшно створено!</b>\n\n"
                 f"{link.link}\n"
                 f"<b>Запитiв: {requests}</b>",
            reply_markup=AdminFactory.link_created(link=callback_data.value)
        )

    except:
        # delete old message
        with suppress(Exception):
            await callback_query.message.delete()

        await callback_query.message.answer(
            text=f"<b>посилання {link.name} успiшно створено!</b>\n\n"
                 f"{link.link}\n"
                 f"<b>Запитiв: {requests}</b>",
            reply_markup=AdminFactory.link_created(link=callback_data.value)
        )
        return


@router.callback_query(AdminFactory.filter(F.action == "my_links"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database,
):
    if await state.get_state() is None:
        date = datetime.now(tz=Configuration.time_zone).strftime("%d.%m.%Y")
        links = await ChannelLink.all_from_database_by(owner_id=int(callback_query.from_user.id), database=database_)
        admin = await Admin.from_database(user_id=int(callback_query.from_user.id), database=database_)
        await state.set_state(AdminStates.process_links_keyboard)
        await state.set_data(dict(admin=admin, links=links, date=date))
    else:
        state_data = await state.get_data()
        date = state_data["date"]
        links = state_data["links"]
        admin = state_data["admin"]
        # check arrows and get a new day
        statistics_date = datetime.strptime(date, "%d.%m.%Y")
        if callback_data.value == "back":
            date = statistics_date - timedelta(days=1)
            date = date.strftime("%d.%m.%Y")
        else:
            date = statistics_date + timedelta(days=1)
            date = date.strftime("%d.%m.%Y")
        await state.update_data(dict(date=date))

    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    text = f"<b>вашi посилання за {date}</b> 🧑🏻‍💼\n\n"
    links_list = []

    for position, link in enumerate(links, start=1):
        if link.created_at == date:
            text += (
                f'{position} - <a href="{link.link}">{link.name}</a>\n'
            )

            links_list.append(position)

    await callback_query.message.answer(
        text=text,
        reply_markup=AdminFactory.link(links_list=links_list)
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "choose_link"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database,
):
    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    links_list = (await state.get_data())["links"]
    link: ChannelLink = links_list[int(callback_data.value) - 1]

    channel = await Channel.from_database(channel_id=link.channel_id, database=database_)
    join_request: int = await JoinRequest.all_from_database_by(link=link.link, database=database_, count=True)
    await callback_query.message.answer(
        text=_menu_text(link=link, channel=channel, join_request=join_request),
        reply_markup=AdminFactory.back()
    )
    await callback_query.answer()


@router.message(F.text == "➕ создать пост")
async def process_message(
        message: Message,
        database_: Database,
):
    channels: list = await Channel.all_from_database(database=database_)
    channels_list = []
    for channel in channels:
        channels_list.append([channel.full_name, str(channel.channel_id)])

    await message.answer(
        text="Выберите канал для создания публикации.",
        reply_markup=AdminFactory.posts.choose_channel(channels=channels_list)
    )


@router.callback_query(AdminFactory.filter(F.action == "create_post"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database,
        state: FSMContext
):
    channel_id = callback_data.value
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)

    await callback_query.message.answer(
        text=f'Пост будет опубликован в канале <a href="https://t.me/{channel.username}"><b>{channel.full_name}</b></a>\n\nТеперь отправьте боту то, что хотите опубликовать.'
    )
    await state.set_data(dict(channel_id=channel_id, channel_username=channel.username, channel_full_name=channel.full_name))
    await state.set_state(AdminStates.create_post)


@router.message(StateFilter(AdminStates.create_post))
async def process_message(
        message: Message,
        bot: Bot,
        database_: Database,
        state: FSMContext,
):
    post = await Post.from_database(post_id=9999999999999, database=database_)
    state_data = await state.get_data()
    post.channel_id = int(state_data["channel_id"])
    post.creator_id = message.from_user.id
    await post.commit()
    if message.text:
        post.content = message.html_text
        await post.commit()
        await state.update_data(data=dict(post=post))
        msg = await bot.send_message(
            text=message.html_text,
            chat_id=message.from_user.id,
            reply_markup=AdminFactory.posts.post_settings()
        )   
        await state.set_state(MassSendStates.post)   

    # photos, videos, animations
    elif message.caption:
        if message.photo:
            photo_id: str = message.photo[-1].file_id
            post.content = {"photo_id": photo_id, "caption": message.html_text}
            await post.commit()
            await state.update_data(data=dict(post=post))
            msg = await bot.send_photo(
                caption=message.html_text,
                chat_id=message.from_user.id,
                photo=photo_id,
                reply_markup=AdminFactory.posts.post_settings()
            )
            await state.set_state(MassSendStates.post)
        elif message.video:
            video_id: str = message.video.file_id
            post.content = {"video_id": video_id, "caption": message.html_text}
            await post.commit()
            await state.update_data(data=dict(post=post))
            msg = await bot.send_video(
                caption=message.html_text,
                chat_id=message.from_user.id,
                video=video_id,
                reply_markup=AdminFactory.posts.post_settings()
            )
            await state.set_state(MassSendStates.post)
        elif message.animation:
            animation_id: str = message.animation.file_id
            post.content = {"animation_id": animation_id, "caption": message.html_text}
            await post.commit()
            await state.update_data(data=dict(post=post))
            msg = await bot.send_animation(
                caption=message.html_text,
                chat_id=message.from_user.id,
                animation=animation_id,
                reply_markup=AdminFactory.posts.post_settings()
            )
            await state.set_state(MassSendStates.post)

            
#початок 1 сторінки

@router.callback_query(F.data == "plan_post")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    state_data = await state.get_data()
    username = state_data["channel_username"]
    full_name = state_data["channel_full_name"]
    await callback_query.message.answer(
        text=f'Пост готов к публикации в канале <a href="https://t.me/{username}"><b>{full_name}</b></a>.\n'
             'Опубликуем сейчас или запланируем на будущее?',
        reply_markup=AdminFactory.posts.post_plan()
    )

@router.callback_query(F.data == "post")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()
    post = state_data["post"]
    try:
        if post.content["photo_id"]:
            await bot.send_photo(
                chat_id=post.channel_id,
                caption=post.content["caption"],
                photo=post.content["photo_id"],
            )
    except:
        try:
            if post.content["video_id"]:
                await bot.send_video(
                    chat_id=post.channel_id,
                    caption=post.content["caption"],
                    video=post.content["video_id"],
                )
        except:
            try:
                if post.content["animation_id"]:
                   await bot.send_animation(
                        chat_id=post.channel_id,
                        caption=post.content["caption"],
                        animation=post.content["animation_id"],
                    )
            except:
                await bot.send_message(
                    chat_id=post.channel_id,
                    text=post.content,
                )


@router.callback_query(F.data == "change_description")
async def process_callback_query(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    await callback_query.message.answer("Отправьте боту исправленный текст.")
    await state.set_state(AdminStates.change_description)


@router.message(StateFilter(AdminStates.change_description))
async def process_message(
        message: Message,
        state: FSMContext,
        database_: Database,
        bot: Bot
):
    with suppress(Exception):
        await message.delete(message_id=message.message_id)

    state_data = await state.get_data()
    post = state_data["post"]
    p = await Post.from_database(post_id=post.post_id, database=database_)

    if isinstance(p.content, str):
        p.content = message.html_text
        await p.commit()
        await state.update_data(data=dict(post=p))
        msg = await bot.send_message(
            text=message.html_text,
            chat_id=message.from_user.id,
            reply_markup=AdminFactory.posts.post_settings()
        )

    else:
        p.content["caption"] = message.html_text
        await p.commit()
        try:
            if p.content["photo_id"]:
                await bot.send_photo(
                    chat_id=message.from_user.id,
                    caption=p.content["caption"],
                    photo=p.content["photo_id"],
                    reply_markup=AdminFactory.posts.post_settings()
                )
        except:
            try:
                if p.content["video_id"]:
                    await bot.send_video(
                        chat_id=message.from_user.id,
                        caption=p.content["caption"],
                        video=p.content["video_id"],
                        reply_markup=AdminFactory.posts.post_settings()
                    )
            except:
                if p.content["animation_id"]:
                    await bot.send_animation(
                        chat_id=message.from_user.id,
                        caption=p.content["caption"],
                        animation=p.content["animation_id"],
                        reply_markup=AdminFactory.posts.post_settings()
                    )


