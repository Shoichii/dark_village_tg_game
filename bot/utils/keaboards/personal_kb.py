from aiogram import types

from utils.consts import CREATURES


poll_creature_buttons_data = 'select_creature'
actions_buttons_data = ('select_action_infect', 'select_action_kill')


def select_action_kb():
    types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='Заразить',
                    callback_data=actions_buttons_data[0]),
                types.InlineKeyboardButton(
                    text='Убить',
                    callback_data=actions_buttons_data[1]),
            ]
        ],
        resize_keyboard=True,
    )
