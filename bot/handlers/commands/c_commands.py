from aiogram import types
from aiogram.filters import Command

import bot.db.common as db_common
from bot.loader import router, bot
from bot.utils.handlers_funcs.c_commands_handlers import check_reg_and_commands
from utils.common import MIN_PLAYERS, STATUS


### команды в чат ###


@router.message(Command('init_game'))
async def init_game_handler(msg: types.Message):
    '''Инициализация игр'''

    # проверка доступа к команде
    accept = await check_reg_and_commands(msg, msg.from_user.id, msg.chat.id)
    if not accept:
        return

    # инициализация игры
    was_game_init = await db_common.initialize_game(msg.chat.id, msg.from_user.id)
    if not was_game_init:
        await bot.send_message(msg.chat.id, text='Игра уже инициализирована')
        return

    await bot.send_message(msg.chat.id, text=f'Игра инициализирована. Ожидаем игроков(минимум {MIN_PLAYERS})')


@router.message(Command('stop_game'))
async def stop_game_handler(msg: types.Message):
    '''Отмена игры'''

    # проверка доступа к команде
    accept = await check_reg_and_commands(msg, msg.from_user.id, msg.chat.id)
    if not accept:
        return

    # информация об игре
    game_info = await db_common.get_game_info(chat_tg_id=msg.chat.id, player_tg_id=msg.from_user.id)

    # если игра не создана
    if not game_info:
        await msg.reply('Игра не создана')
        return

    # если команду отправил не создатель игры
    user_in_chat = await bot.get_chat_member(msg.chat.id, game_info.get('creator_tg_id'))
    user_in_chat = user_in_chat.status != 'left'
    if msg.from_user.id != game_info.get('creator_tg_id') and user_in_chat:
        await msg.reply('''Остановить игру может только её создатель.
''')
        return
    # игра отменена
    await db_common.stop_game(game_info.get('game'))
    await msg.answer('Игра отменена')


@router.message(Command('join_game'))
async def join_players(msg: types.Message):
    '''Присоединится к игре'''

    # проверка доступа к команде
    accept = await check_reg_and_commands(msg, msg.from_user.id, msg.chat.id)
    if not accept:
        return

    # если игры не создана
    game_info = await db_common.get_game_info(chat_tg_id=msg.chat.id, player_tg_id=msg.from_user.id)

    if not game_info:
        await msg.reply('Игра не инициирована или уже началась')
        return

    # если команду отправил создатель игры
    # или игрок который уже присоединился
    found_player = [player for player in game_info.get('players')
                    if player.tg_id == msg.from_user.id]
    if game_info.get('creator_tg_id') == msg.from_user.id \
            or found_player:
        await msg.reply('Вы уже участник игры')
        return

    # проверка достаточности игроков для присоединения
    await db_common.join_game(game_info.get('game'), game_info.get('player'))
    await msg.reply('Вы присоединился к игре')

    players_count = game_info.get('players_count') + 1
    if players_count >= MIN_PLAYERS:
        await msg.answer(f'''Набралось минимальное число игроков.
Всего присоединилось: {players_count}
Можно начать игру с помощью /start_game''')


@router.message(Command('start_game'))
async def start_game_handler(msg: types.Message):
    '''Начать игру'''

    # проверка доступа к команде
    accept = await check_reg_and_commands(msg, msg.from_user.id, msg.chat.id)
    if not accept:
        return

    # информация об игре
    game_info = await db_common.get_game_info(chat_tg_id=msg.chat.id, player_tg_id=msg.from_user.id)

    # если игра не создана
    if not game_info:
        await msg.reply('Игра не создана')
        return

    if game_info.get('status') == STATUS[1][0]:
        await msg.reply('Игра уже началась')
        return

    # проверка кто отправил команду и создана ли игра
    if msg.from_user.id != game_info.get('creator_tg_id'):
        await msg.reply('Начать игру может только её создатель.')
        return

    # проверка достаточности игроков для начала игры
    enough_players = game_info.get('players_count')
    if enough_players < MIN_PLAYERS:
        await msg.answer(f'''Присоединилось недостаточно игроков - {enough_players}.
Необходимо минимум {MIN_PLAYERS}''')
        return

    # начало игры и расдача ролей
    await db_common.start_game(game_info.get('game'))
    await msg.answer('Игра началась')
