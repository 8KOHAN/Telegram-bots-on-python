from aiogram.fsm.state import State, StatesGroup


class MassSendStates(StatesGroup):

    type_users = State()
    post = State()
    buttons = State()
