from asgiref.sync import sync_to_async
from base.models import User, Game
from bot.utils.other import game_init_statuses


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
def initialize_game(chat_tg_id, user):
    '''Инициализация игры'''
    game = Game.objects.filter(chat_id=chat_tg_id).first()

    if game:
        return False

    Game.objects.create(chat_id=chat_tg_id, creator=user)
    return True


@sync_to_async
def stop_game(creator_tg_id):
    '''Отмена игры'''
    creator = User.objects.filter(tg_id=creator_tg_id).first()
    game = Game.objects.filter(creator=creator).first()
    if not game or (game and game.creator.tg_id != creator_tg_id):
        return False
    game.delete()
    return True


@sync_to_async
def join_game(chat_tg_id, player_tg_id):
    '''Присоединится к игре'''
    game = Game.objects.filter(chat_tg_id=chat_tg_id).first()
    if game:
        user = User.objects.filter(tg_id=player_tg_id).first()
        game.players.add(user)
        game.save()
