from datetime import datetime, timedelta
from contextlib import suppress
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.factories import AdminFactory
from bot.fsm.states import AdminStates, SuperAdminStates
from bot.core.database import Database
from bot.core.entities import Admin, Channel
from bot.core.configuration import Configuration

router = Router()


@router.callback_query(AdminFactory.filter(F.action == "choose_a_stat"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database
):

    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get admin from database
    admin = await Admin.from_database(user_id=int(callback_data.value), database=database_)

    # get admin links and requests count
    total_requests_count = 0
    admin_links = await ChannelLink.all_from_database_by(owner_id=admin.user_id, database=database_)
    for link in admin_links:
        # get requests count
        total_requests_count = total_requests_count + await JoinRequest.all_from_database_by(link=link.link, database=database_, count=True)

    # set state and data
    await state.set_state(SuperAdminStates.process_admin_statistics)
    await state.set_data(dict(admin=admin, date="all", admin_links=admin_links))

    # send statistics
    await callback_query.message.answer(
        text=f'<b>статистика по адміністратору за весь час</b> ℹ️\n'
             f'запитiв: {total_requests_count}',

        reply_markup=AdminFactory.statistics.admin(date="all")
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "admin_stat"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database
):
    # check request
    if callback_data.value == "-":
        await callback_query.answer("порожньо", show_alert=True)
        return

    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get state data
    state_data = await state.get_data()
    admin = state_data["admin"]
    date = state_data["date"]
    admin_links = state_data["admin_links"]

    # check date
    if date == "all":
        is_all = True
        date = datetime.now(tz=Configuration.time_zone).strftime("%d.%m.%Y")
    else:
        is_all = False
        statistics_date = datetime.strptime(date, "%d.%m.%Y")

        dates = []
        # check arrows and get a new day
        if callback_data.value == "back":
            for i in range(8):
                dates.append((statistics_date - timedelta(days=i)).strftime("%d.%m.%Y"))
            date = statistics_date - timedelta(days=7)
            date = date.strftime("%d.%m.%Y")
        else:
            for i in range(8):
                dates.append((statistics_date + timedelta(days=i)).strftime("%d.%m.%Y"))
            date = statistics_date + timedelta(days=7)
            date = date.strftime("%d.%m.%Y")

    # get requests by date
    total_requests_count = {}
    for link in admin_links:
        # get requests count
        if is_all:
            total_requests_count[date] = await JoinRequest.all_from_database_by(link=link.link, created_at=date, database=database_, count=True)
        else:
            for date_ in dates:
                total_requests_count[date_] = await JoinRequest.all_from_database_by(link=link.link, created_at=date_, database=database_, count=True)

    # update data
    await state.update_data(dict(date=date))

    # make text
    text = ""
    for date_, requests_count in total_requests_count.items():
        text += f"{date_}: {requests_count}\n"

    # send statistics
    await callback_query.message.answer(
        text=f'<b>статистика по адміністратору</b> ℹ️\n\n'
             f'<code>{text}</code>',
        reply_markup=AdminFactory.statistics.admin()
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "choose_c_stat"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database
):

    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get channel from database
    channel = await Channel.from_database(channel_id=int(callback_data.value), database=database_)

    # get channel links and requests count
    total_requests_count = await JoinRequest.all_from_database_by(channel_id=channel.channel_id, database=database_, count=True)

    # set state and data
    await state.set_state(SuperAdminStates.process_channel_statistics)
    await state.set_data(dict(channel=channel, date="all"))

    # send statistics
    await callback_query.message.answer(
        text=f'<b>статистика по каналу за весь час</b> ℹ️\n'
             f'запитiв: {total_requests_count}',

        reply_markup=AdminFactory.statistics.channel(date="all")
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "channel_stat"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        state: FSMContext,
        database_: Database
):
    # check request
    if callback_data.value == "-":
        await callback_query.answer("порожньо", show_alert=True)
        return

    # delete old message
    with suppress(Exception):
        await callback_query.message.delete()

    # get state data
    state_data = await state.get_data()
    channel = state_data["channel"]
    date = state_data["date"]

    # check date
    if date == "all":
        is_all = True
        date = datetime.now(tz=Configuration.time_zone).strftime("%d.%m.%Y")
    else:
        is_all = False
        statistics_date = datetime.strptime(date, "%d.%m.%Y")

        dates = []
        # check arrows and get a new day
        if callback_data.value == "back":
            for i in range(8):
                dates.append((statistics_date - timedelta(days=i)).strftime("%d.%m.%Y"))
            date = statistics_date - timedelta(days=7)
            date = date.strftime("%d.%m.%Y")
        else:
            for i in range(8):
                dates.append((statistics_date + timedelta(days=i)).strftime("%d.%m.%Y"))
            date = statistics_date + timedelta(days=7)
            date = date.strftime("%d.%m.%Y")

    # get requests by date
    total_requests_count = {}
    # get requests count
    if is_all:
        total_requests_count[date] = await JoinRequest.all_from_database_by(channel_id=channel.channel_id, created_at=date, database=database_, count=True)
    else:
        for date_ in dates:
            total_requests_count[date_] = await JoinRequest.all_from_database_by(channel_id=channel.channel_id, created_at=date_, database=database_, count=True)

    # make text
    text = ""
    for date_, requests_count in total_requests_count.items():
        text += f"{date_}: {requests_count}\n"

    # update data
    await state.update_data(dict(date=date))

    # send statistics
    await callback_query.message.answer(
        text=f'<b>статистика по каналу</b> ℹ️\n'
             f'<code>{text}</code>',
        reply_markup=AdminFactory.statistics.channel()
    )

    # close callback
    await callback_query.answer()


@router.callback_query(AdminFactory.filter(F.action == "l_stat"))
async def process_callback_query(
        callback_query: CallbackQuery,
        callback_data: AdminFactory,
        database_: Database
):
    # delete old message
    # with suppress(Exception):
    #    await callback_query.message.delete()

    # get state data
    channel_link = await ChannelLink.from_database(link=f"https://t.me/{callback_data.value}", database=database_)

    # get requests by date
    all_requests = await JoinRequest.all_from_database_by(link=channel_link.link, database=database_)

    # get requests
    requests = {}
    for request in all_requests:
        if request.created_at in requests.keys():
            requests[request.created_at] += 1
        else:
            requests[request.created_at] = 1

    requests = dict(sorted(requests.items(), key=lambda x: x[0]))
    
    # make requests text
    text = ""

    for request in requests.items():
        text += f"{request[0]}: {request[1]}\n"

    # send statistics
    await callback_query.message.answer(
        text=f'<b>статистика {channel_link.name}</b> ℹ️\n'
             f"<code>{text}</code>"
             f'запитів: {len(all_requests)}, активних: {await User.all_from_database_by_link(link=channel_link.link, database=database_, count=True)}, всього {channel_link.total_users}',
        reply_markup=AdminFactory.back()
    )

    # close callback
    await callback_query.answer()

