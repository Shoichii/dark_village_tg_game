from aiogram.fsm.state import State, StatesGroup


class ProfileDataState(StatesGroup):
    registration = State()
    gender = State()
    birthday = State()
