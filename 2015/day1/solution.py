from pathlib import Path
from itertools import accumulate


def floor_change(par):
    return 1 if par == '(' else -1


def solve_part1(floor_changes):
    return sum(floor_changes)


def solve_part2(floor_changes):
    return 1 + next(pos for pos, acc in enumerate(accumulate(floor_changes)) if acc == -1)


parentheses = Path('input.txt').read_text()
floor_changes = list(map(floor_change, parentheses))

print(solve_part1(floor_changes))
print(solve_part2(floor_changes))
