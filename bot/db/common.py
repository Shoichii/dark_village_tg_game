from datetime import datetime
from asgiref.sync import sync_to_async
from base.models import GameProcessJournal, User, Game, Role
from bot.utils.db import get_two_distinct_random_numbers
from utils.consts import CREATURES, STATUS
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
def one_player_one_game_check(user_tg_id):
    '''Проверка. Можно участвовать только в одной игре за раз'''
    user = User.objects.filter(tg_id=user_tg_id).first()
    game_process_entry = GameProcessJournal.objects.filter(
        player_in_game=user).first()

    return game_process_entry is not None


@sync_to_async
def initialize_game(chat_tg_id, user_tg_id):
    '''Инициализация игры'''
    user = User.objects.filter(tg_id=user_tg_id).first()
    game = Game.objects.filter(chat_id=chat_tg_id).exclude(
        status__in=(STATUS[2][0], STATUS[1][0])).first()

    if game:
        return False

    with transaction.atomic():
        game = Game.objects.create(chat_id=chat_tg_id, creator=user)
        game.players.add(user)
    return True


@sync_to_async
def stop_game(game):
    '''Отмена игры'''
    GameProcessJournal.objects.filter(
        inited_game=game
    ).delete()
    game.status = STATUS[2][0]
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
        # Запись игроков в журнал процесса игры
        GameProcessJournal.objects.create(
            inited_game=game,
            player_in_game=player
        )

    game.status = STATUS[4][0]
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
            status__in=[STATUS[1][0], STATUS[2][0]]).first()

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
        status__in=(STATUS[2][0], STATUS[1][0])).first()
    GameProcessJournal.objects.filter(
        inited_game=game, player_in_game=player
    ).delete()

    if game:
        game.players.remove(player)
        game.save()
        return True
    return False


@sync_to_async
def get_game_process_info(game=None, user_tg_id=None):
    '''Получить информацию о процессе игры'''
    if not game and not user_tg_id:
        raise ValueError(
            "Должен быть передан хотя бы один параметр: game или user_tg_id")

    if game:
        game_process_info = GameProcessJournal.objects.filter(
            inited_game=game).all()

    if user_tg_id:
        user = User.objects.filter(tg_id=user_tg_id).first()
        game = Game.objects.filter(players=user).exclude(
            status__in=(STATUS[2][0], STATUS[1][0])).first()
        game_process_info = GameProcessJournal.objects.filter(
            inited_game=game).all()

    game_info = []
    for info in game_process_info:
        game_info.append({
            'id': info.id,
            'inited_game': info.inited_game,
            'player_in_game': info.player_in_game,
            'voted': info.voted,
            'selected_action': info.selected_action,
            'selected_race': info.selected_race,
            'selected_victim': info.selected_victim,
            'current_buffs': [buff for buff in info.current_buffs.all()],
            'current_debuffs': [debuff for debuff in info.current_debuffs.all()]
        })

    return game_info
