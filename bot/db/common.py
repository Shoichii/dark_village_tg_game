from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import User, Game, Role, StoryText
from bot.utils.db import get_two_distinct_random_numbers
from utils.consts import CREATURES, STATUS
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
    roles = Role.objects.all()
    boss_number, vampire_number = get_two_distinct_random_numbers(
        len(game.players.all()) - 1)
    human_boss = None
    vampire_boss = None
    players_list = []
    for i, player in enumerate(game.players.all()):
        if i == boss_number:
            player.player_role = roles.filter(
                boss=True, gender=player.gender, creature=CREATURES[0][0]).first()
            human_boss = player
        elif i == vampire_number:
            player.player_role = roles.filter(
                boss=True, gender=player.gender, creature=CREATURES[1][0]).first()
            vampire_boss = player
        else:
            player.player_role = roles.filter(
                boss=False, gender=player.gender).first()
            players_list.append(player)
        player.save()

    game.status = STATUS[1][0]
    game.save()
    players = []
    if players_list:
        for player in players_list:
            players.append({
                'player': player,
                'abilities': [ability for ability in player.player_role.abilities.all()]
            })

    data = {
        'human_boss': human_boss,
        'human_boss_abilities': [ability for ability in human_boss.player_role.abilities.all()],
        'vampire_boss': vampire_boss,
        'vampire_boss_abilities': [ability for ability in vampire_boss.player_role.abilities.all()],
        'players': players,
    }
    return data


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


@sync_to_async
def delete_player(chat_id, player_tg_id):
    '''Удаление игрока из игры'''
    player = User.objects.filter(tg_id=player_tg_id).first()
    game = Game.objects.filter(chat_id=chat_id, players=player).exclude(
        status=STATUS[3][0]).first()

    if game:
        game.players.remove(player)
        game.save()
        return True
    return False


@sync_to_async
def get_rules():
    '''Получить правила игры'''
    rules = StoryText.objects.first()
    return rules.rules_text if rules else None


@sync_to_async
def get_about():
    '''Получить инфу об игре'''
    about = StoryText.objects.first()
    return about.about_game_text if about else None
