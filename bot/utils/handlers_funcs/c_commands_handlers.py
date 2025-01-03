from aiogram import types
import bot.db.common as db_common
from bot.loader import bot
from collections import Counter


async def calc_most_votes(votes):
    '''Расчёт результата голосования
    (варианты получившие наибольшее кол-во голосов)'''
    counts = Counter(votes)
    max_count = max(counts.values())
    most_frequent = [action for action,
                     count in counts.items() if count == max_count]
    return most_frequent


async def check_reg_and_commands(*args):
    '''Проверка регистрации пользователя
    и место выполнения команды'''

    msg, user_id, chat_id = args
    accept = True

    # зареган ли пользователь
    user = await db_common.get_user(user_id)
    if not user:
        await msg.reply('Пожалуйста, сначала зарегистрируйся(пиши в лс)')
        accept = False

    # если команда вызвана в лс у бота
    if chat_id == user_id:
        await msg.answer('Команда выполняется только в общем чате')
        accept = False

    return accept


async def check_access(msg, text='Игра не создана'):
    '''Некоторые проверки по доступу к командам'''

    # проверка доступа к команде
    accept = await check_reg_and_commands(msg, msg.from_user.id, msg.chat.id)
    if not accept:
        return False, None

    # информация об игре
    game_info = await db_common.get_game_info(chat_tg_id=msg.chat.id, player_tg_id=msg.from_user.id)

    # если игра не создана
    if not game_info:
        await msg.reply(text)
        return False, None

    return True, game_info


async def get_player_tg_name_in_link(tg_id):
    '''Информация о игроке из телеграма по tg_id'''
    try:
        player = await bot.get_chat(tg_id)
        return f'<a href="tg://user?id={player.id}">{player.full_name}</a>'
    except Exception as e:
        print(e)
        return 'Игрок не найден'


async def get_role_info(role, role_abilities):
    '''Формирование информации о роли'''
    image_path = role.player_role.image.path
    photo = types.FSInputFile(image_path)

    # описание способностей
    abilities_text = ''
    if role_abilities:
        for i, ability in enumerate(role_abilities):
            abilities_text += f'''<b>{i+1}) {ability.name}</b>
{ability.description}

'''

    # описание роли
    boss = '\n<b>Уровень Босс</b>' if role.player_role.boss else ''
    role_decription = f'''Ваша роль: {role.player_role.name}
{boss}
<b>Раса:</b> {role.player_role.get_creature_display()}
<b>Способности:</b>
{abilities_text}

<b>Описание роли:</b>
{role.player_role.description}
'''
    return role_decription, photo, role.tg_id
