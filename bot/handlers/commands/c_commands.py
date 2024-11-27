from aiogram import types
from aiogram.filters import Command

import bot.db.common as db_common
from bot.loader import router, bot
from bot.utils.handlers_funcs.c_commands_handlers import check_access, check_reg_and_commands, get_player_info, get_role_info
from utils.consts import MIN_PLAYERS, STATUS


### команды в чат ###

# init_game - инициировать игру
# join_game - присоединится к игре
# start_game - начать игру
# stop_game - остановить игру
# quit_game - покинуть игру
# list_players - список игроков в игре
# rules - правила
# about - информация об игре


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

    # проверка взаимодействия и доступа
    access = await check_access(msg)
    if not access[0]:
        return
    # информация об игре
    game_info = access[1]

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

    # проверка взаимодействия и доступа
    access = await check_access(msg, 'Игра не инициирована или уже началась')
    if not access[0]:
        return
    # информация об игре
    game_info = access[1]

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

    # проверка взаимодействия и доступа
    access = await check_access(msg)
    if not access[0]:
        return
    # информация об игре
    game_info = access[1]

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
    roles_data = await db_common.start_game(game_info.get('game'))

    # сообщаем старосте деревни его роль
    human_boss_decription, \
        human_boss_photo, \
        human_boss_tg_id = await get_role_info(
            roles_data.get('human_boss'),
            roles_data.get('human_boss_abilities'))
    await bot.send_photo(chat_id=human_boss_tg_id, photo=human_boss_photo, caption=human_boss_decription)
    human_boss_name = await get_player_info(human_boss_tg_id)
    await msg.answer(f'Игра началась\n\nСтароста деревни - {human_boss_name}')

    # сообщаем главному вампиру его роль
    vampire_boss_decription, \
        vampire_boss_photo, \
        vampire_boss_tg_id = await get_role_info(
            roles_data.get('vampire_boss'),
            roles_data.get('vampire_boss_abilities'))
    await bot.send_photo(chat_id=vampire_boss_tg_id, photo=vampire_boss_photo, caption=vampire_boss_decription)


@router.message(Command('quit_game'))
async def quit_game_handler(msg: types.Message):
    '''Выйти из игры'''

    # проверка взаимодействия и доступа
    access = await check_access(msg)
    if not access[0]:
        return
    # информация об игре
    game_info = access[1]

    # проверка кто отправил команду и создана ли игра
    if msg.from_user.id == game_info.get('creator_tg_id'):
        await msg.reply('Создатель игры не может её покинуть до её окончания.')
        return

    # удаление игрока
    was_delete = await db_common.delete_player(msg.chat.id, msg.from_user.id)
    if was_delete:
        await msg.reply('Вы покинули игру')
    else:
        await msg.reply('Вы не состоите в игре')


@router.message(Command('list_players'))
async def list_players_handler(msg: types.Message):
    '''Посмотреть список игроков в игре'''
    # проверка взаимодействия и доступа
    access = await check_access(msg)
    if not access[0]:
        return
    # информация об игре
    game_info = access[1]

    # формирование списка
    players = game_info.get('players')
    players_info_list = 'Игроки в игре: \n\n'
    for i, player in enumerate(players):
        try:
            player_name = await get_player_info(player.tg_id)
            creator = '- инициатор игры' if player.id == game_info.get(
                'creator_tg_id') else ''
            players_info_list += f'{i + 1}) {player_name} {creator}\n'
        except Exception as e:
            print(f"Не удалось получить данные пользователя: {e}")
            return None

    # отправка списка игроков в чате
    await bot.send_message(msg.chat.id, players_info_list, parse_mode="HTML")


@router.message(Command('rules'))
async def rules_handler(msg: types.Message):
    '''Показать правила'''
    rules = await db_common.get_rules()
    await msg.answer(rules)


@router.message(Command('about'))
async def about_handler(msg: types.Message):
    '''Показать инфу об игре'''
    about = await db_common.get_about()
    await msg.answer(about)
