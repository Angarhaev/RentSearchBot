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

    apartment = State()
    area_min = State()
    are_max = State()
    floor = State()
    furniture = State()


