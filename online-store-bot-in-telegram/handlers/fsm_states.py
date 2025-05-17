from aiogram.fsm.state import StatesGroup, State

class AddProduct(StatesGroup):
    choosing_category = State()
    entering_name = State()
    entering_desc = State()
    entering_price = State()
    uploading_photo = State()
