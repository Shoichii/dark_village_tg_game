from aiogram import types
from aiogram.filters import Command

import bot.db.common as db_common
from bot.loader import router, bot
from bot.utils.other import game_init_statuses


### команды в чат ###


@router.message(Command('init'))
async def init_game_handler(msg: types.Message):
    '''Инициализация игр'''

    # зареган ли пользователь
    user = db_common.get_user(msg.from_user.id)
    if not user:
        await msg.reply('Пожалуйста, сначала зарегистрируйся(пиши в лс)')

    # если команда вызвана в лс у бота
    if msg.chat.id == msg.from_user.id:
        await msg.answer('Начать игру можно только в чате')
        return

    # инициализация игры
    was_game_init = await db_common.initialize_game(msg.chat.id, user)
    if was_game_init == game_init_statuses[1]:
        await bot.send_message(msg.chat.id, text='Игра уже инициализирована')
        return

    await bot.send_message(msg.chat.id, text='Игра инициализирована. Ожидаем игроков(минимум 5)')


@router.message(Command('stop'))
async def stop_game_handler(msg: types.Message):
    '''Отмена игры'''

    creator_tg_id = msg.from_user.id
    cancel = await db_common.stop_game(creator_tg_id)

    if not cancel:
        await msg.answer('Остановить игру может только её создатель.')
        return
    await msg.answer('Игра отменена')


@router.message(Command('join'))
async def join_players(msg: types.Message):
    '''Присоединится к игре'''

    # если команда вызвана в лс у бота
    if msg.chat.id == msg.from_user.id:
        await msg.answer('Команда выполняется только в общем чате')
        return
