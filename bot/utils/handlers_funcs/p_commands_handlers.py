from bot.loader import bot
from bot.utils.handlers_funcs.c_commands_handlers import get_player_tg_name_in_link
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


def count_persons(persons):
    '''Подсчёт количества членов расы
    и выдача текстового сообщения
    '''

    persons_list_text = ''
    persons_counter = 0
    for i, human in enumerate(persons):
        human_tg_name = get_player_tg_name_in_link(human.tg_id)
        persons_list_text += f'{i+1}) {human_tg_name}\n'
        persons_counter += 1

    return persons_counter, persons_list_text
