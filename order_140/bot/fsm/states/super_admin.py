from aiogram.fsm.state import State, StatesGroup


class SuperAdminStates(StatesGroup):

    add_admin_enter_id = State()
    process_admin_statistics = State()
    process_channel_statistics = State()
