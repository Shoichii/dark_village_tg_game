from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import User, Game, Role, StoryText
from bot.utils.db import get_two_distinct_random_numbers
from utils.consts import CREATURES, STATUS
from django.db import transaction


@sync_to_async
def get_werewolves():
    '''Получить оборотней'''
