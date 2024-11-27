# общие константы
from asyncio import create_subprocess_exec


STATUS = (
    ('waiting', 'Ожидание игроков'),
    ('started', 'Игра началась'),
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
