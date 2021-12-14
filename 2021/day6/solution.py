from pathlib import Path
from functools import cache


def parse_lanternfishes(filename):
    return [int(val) for val in Path(filename).read_text().split(',')]


@cache
def count_children(days_to_first_child, days_left):
    return sum(
        1 + count_children(9, days_left - day)
        for day in range(days_to_first_child, days_left, 7)
    )


def count_lanternfishes(initial, days):
    return len(initial) + sum(count_children(lfish, days) for lfish in initial)


init_lfishes = parse_lanternfishes('input.txt')

assert count_lanternfishes(init_lfishes, 80) == 396210
assert count_lanternfishes(init_lfishes, 256) == 1770823541496
