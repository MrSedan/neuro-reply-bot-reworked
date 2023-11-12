from aiogram.fsm.state import State, StatesGroup


class ChangePost(StatesGroup):
    Text = State()
