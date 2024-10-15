from aiogram import types

# выбрать пол
male_button = 'male'
female_button = 'female'


def select_gender():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text='🙎‍♂️', callback_data=male_button),
                types.InlineKeyboardButton(
                    text='🙍‍♀️', callback_data=female_button),
            ]
        ],
        resize_keyboard=True,
    )
