from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    process_links_keyboard = State()
    enter_link_name = State()
    enter_link_number = State()
    forward_post = State()
    enter_replace_link = State()

    choose_channel = State()
    print_time = State()
    print_time_delete = State()
    posting = State()

    create_post = State()
    change_description = State()
