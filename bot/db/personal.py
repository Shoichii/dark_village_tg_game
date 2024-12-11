from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import Debuff, GameProcessJournal, User, Game, Role, StoryText
from bot.utils.db import get_two_distinct_random_numbers
from utils.consts import CREATURES, STATUS
from django.db import transaction


@sync_to_async
def set_debuff(game, player):
    '''Установить дебафф "Заражение"'''
    debuffs = Debuff.objects.filter(key='infection').first()
    game_journal_entry = GameProcessJournal.objects.filter(
        inited_game=game, player_in_game=player).first()
    game_journal_entry.current_debuffs.add(debuffs)
    game_journal_entry.save()
