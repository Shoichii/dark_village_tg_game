from aiogram import types

from utils.consts import CREATURES


poll_creature_buttons_data = 'select_creature'


def select_creature(user_tg_id):
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='Человек',
                    callback_data=f'{poll_creature_buttons_data}_{user_tg_id}_{CREATURES[0][0]}'),
                types.InlineKeyboardButton(
                    text='Оборотень',
                    callback_data=f'{poll_creature_buttons_data}_{user_tg_id}_{CREATURES[2][0]}'),
            ]
        ],
        resize_keyboard=True,
    )
