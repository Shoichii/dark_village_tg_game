from django.db import models

from utils.consts import CREATURES, STATUS


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

    @property
    def creature_display(self):
        return dict(CREATURES).get(self.creature)

    def __str__(self):
        return f'{self.name} {self.get_gender_display()}'


class Ability(models.Model):
    '''Способность'''
    key = models.CharField(max_length=255, verbose_name='Ключ')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Способность'
        verbose_name_plural = 'Способности'

    def __str__(self):
        return f'{self.key} - {self.name}'


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
    end_time = models.DateTimeField(
        blank=True, null=True, verbose_name='Время окончания игры')

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


class GameProcessJournal(models.Model):
    '''Журнал процесса игры'''
    inited_game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name='Инициированная игра')
    player_in_game = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Игрок', related_name='player_in_game_journal')
    voted = models.BooleanField(default=False, verbose_name='Проголосовал?')
    selected_race = models.CharField(
        max_length=255, choices=CREATURES, null=True, blank=True, verbose_name='Выбранная раса/существо')
    selected_victim = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='выбранная жертва', null=True, blank=True, related_name='selected_victim_journal')
    current_buffs = models.ManyToManyField('Buff', blank=True,)
    current_debuffs = models.ManyToManyField('Debuff', blank=True,)

    class Meta:
        verbose_name = 'Журнал процесса игры'
        verbose_name_plural = 'Журналы процесса игр'

    def __str__(self):
        return f'Журнал игры id - {self.inited_game.id}'


class Buff(models.Model):
    '''Баффы'''
    key = models.CharField(max_length=255, verbose_name='Ключ')
    name = models.CharField(max_length=255, verbose_name='Название баффа')
    description = models.TextField(verbose_name='Описание баффа')

    class Meta:
        verbose_name = 'Бафф'
        verbose_name_plural = 'Баффы'

    def __str__(self):
        return f'{self.key} - {self.name}'


class Debuff(models.Model):
    '''Дебаффы'''
    key = models.CharField(max_length=255, verbose_name='Ключ')
    name = models.CharField(max_length=255, verbose_name='Название дебаффа')
    description = models.TextField(verbose_name='Описание дебаффа')

    class Meta:
        verbose_name = 'Дебафф'
        verbose_name_plural = 'Дебаффы'

    def __str__(self):
        return f'{self.key} - {self.name}'
