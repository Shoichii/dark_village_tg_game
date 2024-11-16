from aiogram import types
from aiogram.filters import Command

import bot.db.common as db_common
from bot.loader import router, bot
from utils.common import MIN_PLAYERS, STATUS


### команды в чат ###


@router.message(Command('init_game'))
async def init_game_handler(msg: types.Message):
    '''Инициализация игр'''

    # зареган ли пользователь
    user = await db_common.get_user(msg.from_user.id)
    if not user:
        await msg.reply('Пожалуйста, сначала зарегистрируйся(пиши в лс)')

    # если команда вызвана в лс у бота
    if msg.chat.id == msg.from_user.id:
        await msg.answer('Начать игру можно только в чате')
        return

    # инициализация игры
    was_game_init = await db_common.initialize_game(msg.chat.id, msg.from_user.id)
    if was_game_init == STATUS[0]:
        await bot.send_message(msg.chat.id, text='Игра уже инициализирована')
        return

    await bot.send_message(msg.chat.id, text=f'Игра инициализирована. Ожидаем игроков(минимум {MIN_PLAYERS})')


@router.message(Command('stop_game'))
async def stop_game_handler(msg: types.Message):
    '''Отмена игры'''
    game_data = await db_common.check_creator_and_game(msg.from_user.id)

    if not game_data:
        await msg.answer('Остановить игру может только её создатель.')
        return
    await db_common.stop_game(game_data[1])
    await msg.answer('Игра отменена')


@router.message(Command('join_game'))
async def join_players(msg: types.Message):
    '''Присоединится к игре'''

    # если команда вызвана в лс у бота
    if msg.chat.id == msg.from_user.id:
        await msg.answer('Команда выполняется только в общем чате')
        return

    players_count = await db_common.join_game(msg.chat.id, msg.from_user.id)
    await msg.reply('Вы присоединился к игре')
    print(players_count)
    if players_count >= MIN_PLAYERS:
        await msg.answer(f'''Набралось минимальное число игроков.
Всего присоединилось: {players_count}
Можно начать игру с помощью /start_game''')


@router.message(Command('start_game'))
async def start_game_handler(msg: types.Message):
    '''Начать игру'''

    start = await db_common.start_game(msg.from_user.id)
    if not start:
        await msg.answer('Начать игру может только её создатель.')
        return
    if isinstance(start, int):
        await msg.answer(f'''Присоединилось недостаточно игроков - {start}.
Необходимо минимум {MIN_PLAYERS}''')
        return
    await msg.answer('Игра началась')
