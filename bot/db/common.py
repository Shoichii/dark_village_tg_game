from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import User, Game, Role
from utils.common import CREATURES, MIN_PLAYERS, STATUS
from random import randint
from django.db import transaction


# информация для общего чата, которая видна всем

@sync_to_async
def get_user(tg_id):
    '''Получить пользователя'''
    user = User.objects.filter(tg_id=tg_id).first()
    return user


@sync_to_async
def create_new_user(tg_id, gender, birthday):
    '''Создать нового пользователя'''
    User.objects.create(tg_id=tg_id, gender=gender, birthday=birthday)


@sync_to_async
def initialize_game(chat_tg_id, user_tg_id):
    '''Инициализация игры'''
    user = User.objects.filter(tg_id=user_tg_id).first()
    game = Game.objects.filter(chat_id=chat_tg_id).exclude(
        status=STATUS[3][0]).first()

    if game:
        return False

    with transaction.atomic():
        game = Game.objects.create(chat_id=chat_tg_id, creator=user)
        game.players.add(user)
    return True


@sync_to_async
def stop_game(game):
    '''Отмена игры'''
    game.status = STATUS[3][0]
    game.end_time = datetime.now()
    game.save()
    return True


@sync_to_async
def join_game(game, player):
    '''Присоединится к игре'''
    game.players.add(player)
    game.save()


@sync_to_async
def start_game(game):
    '''Начать игру'''

    # раздача ролей
    roles = Role.objects.filter(creature=CREATURES[0][0]).all()
    boss_number = randint(0, len(game.players.all()) - 1)
    for i, player in enumerate(game.players.all()):
        if i == boss_number:
            player.player_role = roles.filter(
                boss=True, gender=player.gender).first()
        else:
            player.player_role = roles.filter(
                boss=False, gender=player.gender).first()
        player.save()

    game.status = STATUS[1][0]
    game.save()
    return True


@sync_to_async
def get_game_info(**kwargs):
    '''Информация о игре

    kwargs:

    chat_tg_id: int,
    player_tg_id: int,
    or
    game: Game,
    player: User,

    '''

    chat_tg_id = kwargs.get('chat_tg_id')
    player_tg_id = kwargs.get('player_tg_id')
    game = kwargs.get('game')
    player = kwargs.get('player')

    if not player and not game:
        player = User.objects.filter(tg_id=player_tg_id).first()
        game = Game.objects.filter(chat_id=chat_tg_id).exclude(
            status=STATUS[3][0]).first()

    if not game:
        return None

    return {
        'game': game,
        'player': player,
        'creator_tg_id': game.creator.tg_id,
        'players': [
            player
            for player in game.players.all()
        ],
        'status': game.status,
        'start_time': game.start_time,
        'end_time': game.end_time,
        'chat_id': game.chat_id,
        'players_count': game.players.count(),
    }
