# общие константы
from asyncio import create_subprocess_exec


STATUS = (
    ('waiting', 'Ожидание игроков'),
    ('finished', 'Игра закончилась'),
    ('canceled', 'Игра отменена'),
    ('Day', 'День'),
    ('Night', 'Ночь'),
)


# минимальное количество игроков
MIN_PLAYERS = 2


# существа/расы
CREATURES = (
    ('human', 'Человек'),
    ('vampire', 'Вампир'),
    ('werewolf', 'Оборотень')
)

# действия над жертвами
ACTIONS = (
    ('infect', 'Заразить'),
    ('kill', 'Убить')
)

# ключи дебаффов
DEBUFFS_KEYS = ('infection',)


# количество жертв на выбор для голосования
MAX_VOTE_VICTIMS = 3
