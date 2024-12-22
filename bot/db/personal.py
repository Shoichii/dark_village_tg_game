import bot.utils.handlers_funcs.p_commands_handlers
from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import Debuff, GameProcessJournal, User, Game, Role
from bot.utils.db import get_two_distinct_random_numbers
from utils.consts import ACTIONS, CREATURES, STATUS
from django.db import transaction


@sync_to_async
def set_debuff(game, player):
    '''Установить дебафф "Заражение"'''
    debuffs = Debuff.objects.filter(key='infection').first()
    game_journal_entry = GameProcessJournal.objects.filter(
        inited_game=game, player_in_game=player).first()
    game_journal_entry.current_debuffs.add(debuffs)
    game_journal_entry.save()


@sync_to_async
def set_selected_action(user_tg_id, selected_action):
    '''Запись выбранного действия'''
    user = User.objects.filter(tg_id=user_tg_id).first()
    game = Game.objects.filter(players=user).exclude(
        status__in=(STATUS[2][0], STATUS[1][0])).first()
    journal_entry = GameProcessJournal.objects.filter(
        inited_game=game, player_in_game=user).first()
    journal_entry.selected_action = selected_action
    journal_entry.save()


@sync_to_async
def set_selected_victim(user_tg_id, victim_tg_id):
    '''Запись выбранной жертвы'''
    user = User.objects.filter(tg_id=user_tg_id).first()
    game = Game.objects.filter(players=user).exclude(
        status__in=(STATUS[2][0], STATUS[1][0])).first()
    journal_entry = GameProcessJournal.objects.filter(
        inited_game=game, player_in_game=user).first()
    journal_entry.selected_victim = victim_tg_id
    journal_entry.save()


@sync_to_async
def get_role_creatures(players):
    '''Получить игроков по ролям'''
    humans = []
    vampires = []
    werewolves = []
    for player in players:
        if player.player_role.creature == CREATURES[0][0]:
            humans.append(player)
        if player.player_role.creature == CREATURES[1][0]:
            vampires.append(player)
        if player.player_role.creature == CREATURES[2][0]:
            werewolves.append(player)
    return humans, vampires, werewolves
