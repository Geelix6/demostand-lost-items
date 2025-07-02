from aiogram.fsm.state import State, StatesGroup


class LostState(StatesGroup):
    date = State()
    station = State()
    description = State()
