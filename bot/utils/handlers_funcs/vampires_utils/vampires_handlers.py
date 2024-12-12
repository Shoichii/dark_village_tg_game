

import bot.db.common as db_common
from bot.utils.handlers_funcs.p_commands_handlers import count_persons
from bot.utils.keaboards.personal_kb import select_action_kb
from bot.loader import bot
from utils.consts import DEBUFFS_KEYS


async def send_to_vampires_poll_action_select(*args):
    '''Выбор жертвы у вампиров - опрос'''
    game, humans, vampires, werewolves = args

    # если вампиры голодны, то опрос отменяется
    game_process_info = await db_common.get_game_processes_info(game)
    vampires_tg_ids = [vampire.tg_id for vampire in vampires]
    vampire_hunger = False
    for game_info in game_process_info:
        current_debuffs_keys = [
            debuff for debuff in game_info.get('current_debuffs')]
        if game_info.get('player_in_game').tg_id in vampires_tg_ids and \
                DEBUFFS_KEYS[0] in current_debuffs_keys:
            vampire_hunger = True
            break
    if vampire_hunger:
        # опрос не задан
        return False

    # формирование сообщение со списком жителей
    # для вампиров это оборотни и люди, исключая их самих
    residents_counter, residents_list_text = count_persons(
        [*humans, *werewolves])

    text = f'''На данный момент в деревне {residents_counter} жителей:

{residents_list_text}
'''
    kb = select_action_kb()

    # если вампиров меньше 2х
    if len(vampires) < 2:
        for vampire in vampires:
            # отправка списка жителей
            await bot.send_message(chat_id=vampire.tg_id, text=text)
            # отправка опроса, какое действие совершить
            if vampire.player_role.boss:
                await bot.send_message(chat_id=vampire.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
            else:
                await bot.send_message(chat_id=vampire.tg_id, text='Глава клана выбирает для Вас задачу')
    # если вампиров больше 2х
    else:
        for vampire in vampires:
            # отправка списка жителей
            await bot.send_message(chat_id=vampire.tg_id, text=text)
            # отправка опроса, какое действие совершить
            await bot.send_message(chat_id=vampire.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
    # опрос задан
    return True


# async def send_to_vampires_poll_victim_select(*args):
#     '''Выбор жертвы у вампиров - опрос'''
