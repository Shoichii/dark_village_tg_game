from bot.loader import bot
from bot.db import common as db_common
from bot.utils.keaboards.personal_kb import select_creature
from utils.consts import CREATURES


async def send_photo_to_pm(chat_id, photo, caption=None):
    '''Отправка сообщений с фото в лс'''
    kwargs = {"chat_id": chat_id, "photo": photo}
    if caption is not None:
        kwargs["caption"] = caption
    await bot.send_photo(**kwargs)


async def get_humans(players):
    '''Получить людей'''
    return [player for player in players if player.player_role == CREATURES[0][0]]


async def get_vampires(players):
    '''Получить вампиров'''
    return [player for player in players if player.player_role == CREATURES[1][0]]


async def get_werewolves(players):
    '''Получить оборотней'''
    return [player for player in players if player.player_role == CREATURES[2][0]]


async def send_to_vampires_poll_race_select(*args):
    '''Выбор жертвы у вампиров - опрос'''

    vampires, humans, werewolves = args
    text = '''Уничтожить псину или явиться к человеку?
Выберите расу, чтобы сделать злобный кусь😈'''
    kb = select_creature(vampires[0].tg_id)

    # если есть и люди и вампиры
    if humans and werewolves:
        # # если вампир пока один
        # if len(vampires) == 1:
        #     bot.send_message(vampires[0].tg_id, text, reply_markup=kb)
        #     return True

        # # если два вампира
        # if len(vampires) == 2:
        #     for vampire in vampires:
        #         if
        for vampire in vampires:
            if len(vampires) == 2 and not vampire.player_role.boss:
