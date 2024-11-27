

from random import randint


def get_two_distinct_random_numbers(max_value):
    '''Получить два рандомных числа'''
    first = randint(0, max_value)
    second = randint(0, max_value)
    while second == first:
        second = randint(0, max_value)
    return first, second
