from aiogram import types

from utils.consts import CREATURES


poll_creature_buttons_data = 'select_creature'
actions_buttons_data = ('select_action_infect', 'select_action_kill')
victims_buttons_data = 'select_victim'


def select_action_kb():
    return types.InlineKeyboardMarkup(
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


def select_victim_kb(victims):
    victims_numbers = len(victims)
    inline_keyboard = [
        [
            types.InlineKeyboardButton(
                text='Заразить',
                callback_data=actions_buttons_data[0]),
            types.InlineKeyboardButton(
                text='Убить',
                callback_data=actions_buttons_data[1]),
        ]
    ]
    kb_row = []
    for i, victim in enumerate(victims):
        kb_row.append(
            types.InlineKeyboardButton(
                text=i+1,
                callback_data=f'{victims_buttons_data}_{victim.tg_id}')
        )
        if len(kb_row) % 5 == 0 or i == victims_numbers - 1:
            inline_keyboard.append(kb_row)
            kb_row = []

    return types.InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
        resize_keyboard=True,
    )
