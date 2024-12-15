import random
from bot.loader import bot
from bot.utils.handlers_funcs.c_commands_handlers import calc_most_votes, get_player_tg_name_in_link
from bot.utils.handlers_funcs.p_commands_handlers import count_persons
from bot.utils.keaboards.personal_kb import select_action_kb, select_victim_kb
from utils.consts import CREATURES, DEBUFFS_KEYS, MAX_VOTE_VICTIMS
import bot.db.common as db_common


async def send_photo_to_pm(chat_id, photo, caption=None):
    '''Отправка сообщений с фото в лс'''
    kwargs = {"chat_id": chat_id, "photo": photo}
    if caption is not None:
        kwargs["caption"] = caption
    await bot.send_photo(**kwargs)


async def get_humans(players):
    '''Получить живых людей'''
    return [player for player in players if player.player_role == CREATURES[0][0]]


async def get_vampires(players):
    '''Получить живых вампиров'''
    return [player for player in players if player.player_role == CREATURES[1][0]]


async def get_werewolves(players):
    '''Получить живых оборотней'''
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


async def send_to_dark_creatures_poll_action_select(*args):
    '''Выбор жертвы у вампиров - опрос'''
    game_process_info, humans, vampires, werewolves, creature_is = args

    # если нечисть голодна, то опрос отменяется
    if creature_is == CREATURES[1][0]:
        this_creatures = vampires
        not_this_creature = werewolves
    if creature_is == CREATURES[2][0]:
        this_creatures = werewolves
        not_this_creature = vampires
    this_creatures_tg_ids = [
        this_creature.tg_id for this_creature in this_creatures]
    this_creature_hunger = False
    for game_info in game_process_info:
        current_debuffs_keys = [
            debuff for debuff in game_info.get('current_debuffs')]
        if game_info.get('player_in_game').tg_id in this_creatures_tg_ids and \
                DEBUFFS_KEYS[0] in current_debuffs_keys:
            this_creature_hunger = True
            break
    if this_creature_hunger:
        # опрос не задан
        return False

    # формирование сообщение со списком жителей
    # для вампиров это оборотни и люди, исключая их самих
    # для оборотней это вампиры и люди
    residents_counter, residents_list_text = count_persons(
        [*humans, *not_this_creature])

    text = f'''На данный момент в деревне {residents_counter} жителей:

{residents_list_text}
'''
    kb = select_action_kb()

    # если нечисти меньше 2х
    if len(this_creatures) < 2:
        for this_creature in this_creatures:
            # отправка списка жителей
            await bot.send_message(chat_id=this_creature.tg_id, text=text)
            # отправка опроса, какое действие совершить
            if this_creature.player_role.boss:
                await bot.send_message(chat_id=this_creature.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
            else:
                await bot.send_message(chat_id=this_creature.tg_id, text='Глава клана выбирает для Вас задачу')
    # если нечисти больше 2х
    else:
        for this_creature in this_creatures:
            # отправка списка жителей
            await bot.send_message(chat_id=this_creature.tg_id, text=text)
            # отправка опроса, какое действие совершить
            await bot.send_message(chat_id=this_creature.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
    # опрос задан
    return True


async def send_to_dark_creatures_poll_victim_select(*args):
    '''Опрос о выборе жертвы у нечисти'''
    game_process_info, humans, vampires, werewolves, creature_is = args

    # кто атакует и кого атакуют
    # если нападают вампиры
    if creature_is == CREATURES[1][0]:
        this_creatures = vampires
        potential_victims = [*humans, *werewolves]
    # если нападают оборотни
    if creature_is == CREATURES[2][0]:
        this_creatures = werewolves
        werewolves_tg_ids = [werewolf.tg_id for werewolf in werewolves]
        race_votes = [game_info.selected_race for game_info in game_process_info if game_info.get(
            'player_in_game').tg_id in werewolves_tg_ids]
        selected_race = calc_most_votes(race_votes)[0]
        if selected_race == CREATURES[0][0]:
            potential_victims = [*humans]
        if selected_race == CREATURES[1][0]:
            potential_victims = [*vampires]

    # выявляем жертв для голосования рандомно
    # если потенциальных жертв больше 2х
    if len(potential_victims) > 2:
        poll_victims_number = random.sample(
            range(0, len(potential_victims)+1), MAX_VOTE_VICTIMS)
        poll_victims = [potential_victims[i] for i in poll_victims_number]
    # если равно 2
    elif len(potential_victims) == 2:
        poll_victims = potential_victims
    # если 1
    else:
        # ПОБЕДА если у вампиров остался 1 враг
        # и частичная ПОБЕДА у оборотней так как они выбирают одну расу
        return False

    text = '''Выбирать нужно аккуратно, чтобы убийство прошло незаметно и не поднялся шум.
Вот список, кто подойдёт Вам в этот раз. Выберите жертву.'''
    for i, poll_victim in enumerate(poll_victims):
        poll_victim_tg_name = get_player_tg_name_in_link(poll_victim.tg_id)
        text += f'{i+1}) {poll_victim_tg_name}\n'
    kb = select_victim_kb(poll_victim)

    # если нечисти меньше 2х
    if len(this_creatures) < 2:
        for this_creature in this_creatures:
            # отправка списка жителей
            await bot.send_message(chat_id=this_creature.tg_id, text=text)
            # отправка опроса, какое действие совершить
            if not this_creature.player_role.boss:
                await bot.send_message(chat_id=this_creature.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
            else:
                await bot.send_message(chat_id=this_creature.tg_id, text='Ваш подчинённый выбирает жертву.')
    # если нечисти больше 2х
    else:
        for this_creature in this_creatures:
            # отправка списка жителей
            await bot.send_message(chat_id=this_creature.tg_id, text=text)
            # отправка опроса, какое действие совершить
            await bot.send_message(chat_id=this_creature.tg_id, text='Что вы хотите сделать?', reply_markup=kb)
    # опрос задан
    return True
