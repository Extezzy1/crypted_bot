from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMOffset(StatesGroup):
    type_of_procedure = State()
    enter_phrase = State()
    enter_offset = State()