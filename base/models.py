from django.db import models

from utils.common import CREATURES, STATUS


GENDER = (
    ('male', 'М'),
    ('female', 'Ж'),
)


class User(models.Model):
    '''Пользователь'''
    tg_id = models.BigIntegerField(verbose_name='Telegram ID')
    gender = models.CharField(
        max_length=255, choices=GENDER, verbose_name='Пол')
    birthday = models.DateField(verbose_name='Дата рождения')
    player_role = models.ForeignKey('Role', on_delete=models.CASCADE,
                                    verbose_name='Роль игрока', blank=True, null=True)
    last_action = models.DateTimeField(
        auto_now_add=True, verbose_name='Время последнего действие')
    bought = models.BooleanField(default=False, verbose_name='Игра куплена')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.tg_id)


class Role(models.Model):
    '''Роль'''
    name = models.CharField(max_length=255, verbose_name='Название')
    gender = models.CharField(
        max_length=255, choices=GENDER, verbose_name='Пол')
    creature = models.CharField(
        max_length=255, choices=CREATURES, verbose_name='Существо/раса')
    boss = models.BooleanField(default=False, verbose_name='Босс')
    image = models.ImageField(upload_to='roles/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    abilities = models.ManyToManyField(
        'Ability', blank=True, verbose_name='Способности')

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Ability(models.Model):
    '''Способность'''
    DAMAGE_LEVEL = (
        ('full', 'Полный'),
        ('half', 'Половина'),
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    passive = models.BooleanField(
        default=True, verbose_name='Пассивная/Активная')
    damage = models.CharField(
        max_length=255, choices=DAMAGE_LEVEL, verbose_name='Урон')
    action_time = models.IntegerField(
        default=1, verbose_name='Время действия', null=True, blank=True)

    class Meta:
        verbose_name = 'Способность'
        verbose_name_plural = 'Способности'

    def __str__(self):
        return self.name


class Game(models.Model):
    '''Игра'''

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Создатель игры', related_name='games_created')
    status = models.CharField(
        max_length=255, choices=STATUS, default='waiting', verbose_name='Статус')
    players = models.ManyToManyField(
        User, blank=True, verbose_name='Игроки', related_name='games_joined')
    chat_id = models.BigIntegerField(verbose_name='ID чата')
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Время начала игры')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return str(self.id)


class Achievement(models.Model):
    '''Достижение'''
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='achievements/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return self.name
