from asgiref.sync import sync_to_async
from base.models import User


@sync_to_async
def get_user(tg_id):
    '''Получить пользователя'''
    user = User.objects.filter(tg_id=tg_id).first()
    return user


@sync_to_async
def create_new_user(tg_id, gender, birthday):
    User.objects.create(tg_id=tg_id, gender=gender, birthday=birthday)
