from asgiref.sync import sync_to_async
from base.models import User, Game, Role
from utils.common import CREATURES, MIN_PLAYERS, STATUS
from random import randint
from django.db import transaction


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
def check_creator_and_game(creator_tg_id):
    '''Проверка является ли пользователь создателем игры
    и запущена ли вообще игра'''
    creator = User.objects.filter(tg_id=creator_tg_id).first()
    game = Game.objects.filter(creator=creator).exclude(
        status=STATUS[3][0]).first()
    if not game or (game and game.creator.tg_id != creator.tg_id):
        return None
    return creator, game


@sync_to_async
def stop_game(game):
    '''Отмена игры'''
    game.status = STATUS[3][0]
    game.save()
    return True


@sync_to_async
def join_game(chat_tg_id, player_tg_id):
    '''Присоединится к игре'''
    game = Game.objects.filter(chat_id=chat_tg_id).exclude(
        status=STATUS[3][0]).first()
    if game:
        user = User.objects.filter(tg_id=player_tg_id).first()
        game.players.add(user)
        game.save()
    return len(game.players.all())


@sync_to_async
def check_enough_players(creator_tg_id):
    '''Проверка достаточности игроков'''
    creator = User.objects.filter(tg_id=creator_tg_id).first()
    game = Game.objects.filter(creator=creator).first()
    if not game or (game and game.creator.tg_id != creator_tg_id):
        return False
    return game.players.count() >= MIN_PLAYERS


@sync_to_async
def start_game(creator_tg_id):
    '''Начать игру'''
    creator = User.objects.filter(tg_id=creator_tg_id).first()
    game = Game.objects.filter(creator=creator).first()

    # определяем можно ли начать игру
    if not game or (game and game.creator.tg_id != creator_tg_id):
        return False
    if game.players.count() < MIN_PLAYERS:
        return game.players.count()

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

    game.status = 'started'
    game.save()
    return True
