from pathlib import Path
from functools import reduce


def anyone_answered_yes_count(group):
    return len(reduce(set.union, map(set, group.splitlines())))


def everyone_answered_yes_count(group):
    return len(reduce(set.intersection, map(set, group.splitlines())))


groups = Path('input.txt').read_text().split('\n\n')

part1_result = sum(map(anyone_answered_yes_count, groups))
part2_result = sum(map(everyone_answered_yes_count, groups))

print('part 1:', part1_result)
print('part 2:', part2_result)

assert part1_result == 6903
assert part2_result == 3493
