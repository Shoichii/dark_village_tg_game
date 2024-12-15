from datetime import datetime
import re

from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import bot.db.common as db_common
import bot.db.personal as db_personal
from bot.loader import router
from bot.utils.handlers_funcs.c_commands_handlers import calc_most_votes, get_player_tg_name_in_link
from bot.utils.handlers_funcs.p_commands_handlers import get_humans, get_vampires, get_werewolves, send_to_dark_creatures_poll_victim_select
from bot.utils.keaboards.common_kb import female_button, male_button, select_gender
from bot.utils.other import date_pattern
from bot.utils.states.ProfileDataState import ProfileDataState
from bot.utils.keaboards.personal_kb import actions_buttons_data


### команды в лс боту ###

# start - главная команда. первый раз применяется
# для регистрации

# старт
@router.message(Command('start'), StateFilter('*'))
async def start_handler(msg: types.Message, state: FSMContext):
    '''Главная команда /start'''

    # если команда вызвана не в лс у бота
    if msg.chat.id != msg.from_user.id:
        return

    await state.clear()

    # есть ли такой юзер
    user = await db_common.get_user(msg.from_user.id)
    if not user:
        # процесс регистрации
        await state.update_data(registration=True)
        await msg.answer('Твой пол', reply_markup=select_gender())
    else:
        pass


@router.callback_query(lambda call: call.data == male_button or call.data == female_button)
async def select_gender_handler(call: types.CallbackQuery, state: FSMContext):
    '''Выбор пола'''
    await call.message.delete()
    data = await state.get_data()
    is_registration = data.get('registration')

    if is_registration:
        # записываем пол и спрашиваем дату рождения
        await state.update_data(gender=call.data.split('_')[0])
        await call.message.answer('Твоя дата рождения. Напиши в формате: 01.01.1970')
        await state.set_state(ProfileDataState.birthday)
    else:
        pass


@router.message(StateFilter(ProfileDataState.birthday))
async def set_birthday_handler(msg: types.Message, state: FSMContext):
    '''Установка даты рождения'''
    if not re.match(date_pattern, msg.text):
        await msg.answer('Неверный формат')
        return

    data = await state.get_data()
    gender = data.get('gender')
    birthday = datetime.strptime(msg.text, '%d.%m.%Y').date()

    await db_common.create_new_user(msg.from_user.id, gender, birthday)
    await msg.answer('Регистрация завершена')
    await state.clear()


@router.callback_query(lambda call: call.data in actions_buttons_data)
async def select_action_dark_creatures_handler(call: types.CallbackQuery):
    '''Получаем и записываем в бд, выбранное действие
    для тёмных существ'''
    await call.message.delete()

    # сохраняем действие в бд
    selected_action = call.data.split('_')[2]
    await db_personal.set_selected_action(call.from_user.id, selected_action)

    # узнаём, скольким осталось проголосовать
    game_process_info = await db_common.get_game_process_info(user_tg_id=call.from_user.id)
    player_role = next((game_process.get(
        'player_in_game').player_role for game_process in game_process_info if game_process.get(
        'player_in_game').tg_id == call.from_user.id), None)
    this_creatures = [game_process for game_process in game_process_info if game_process.get(
        'player_in_game').player_role == player_role[0]]

    # если больше 2
    not_voted_players = []
    selected_actions = []
    for process_info in this_creatures:
        # сколько и кто не проголосовал
        if process_info.get('selected_action') is None:
            player = process_info.get('player_in_game')
            not_voted_players.append(player.tg_id)
        # сколько проголосовало и за что
        if process_info.get('selected_action') is not None:
            selected_actions.append(process_info.get('selected_action'))

    # если есть кто не проголосовал
    if not_voted_players:
        text = 'Ваш выбор принят. Ещё выбирают:\n\n'
        for i, no_voted_player in enumerate(not_voted_players):
            player_name = await get_player_tg_name_in_link(no_voted_player)
            text += f'{i+1}) {player_name}\n'
        await call.message.answer(text)
        return

    # если проголосовали все
    if not not_voted_players:
        # находим выбор с наибольшим количеством голосов
        votes_result = calc_most_votes(selected_actions)
        # если есть один вариант с большим кол-вом голосов
        if len(votes_result) == 1:
            # данные для опроса по жертве
            players = [game_process.get('player_in_game')
                       for game_process in game_process_info]
            humans = get_humans(players)
            vampires = get_vampires(players)
            werewolves = get_werewolves(players)
            poll_was_send = await send_to_dark_creatures_poll_victim_select(game_process_info,
                                                                            humans, vampires, werewolves, player_role[0])
        # если несколько вариантов с одинаковым кол-вом голосов
        else:
            # выбор делает вожак в спорной ситуации !!!!!!!!!!!!!!!!
            pass
