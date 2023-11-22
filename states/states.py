from aiogram.fsm.state import default_state, StatesGroup, State


class AlSettings(StatesGroup):
    start = State()
    settings = State()
    metro = State()
    min_price = State()
    max_price = State()
    max_price_2 = State()
    amount_rooms = State()
    swipe = State()

    update = State()
    update_min = State()
    update_max = State()
    update_disrict = State()
    update_rooms = State()
    update_finish = State()

