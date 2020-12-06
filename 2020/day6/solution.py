from pathlib import Path
from functools import reduce


def anyone_answered_yes_count(group):
    return len(set(group.replace('\n', '')))


def everyone_answered_yes_count(group):
    return len(reduce(set.intersection, (set(line) for line in group.splitlines())))


groups = Path('input.txt').read_text().split('\n\n')

part1_result = sum(map(anyone_answered_yes_count, groups))
part2_result = sum(map(everyone_answered_yes_count, groups))

print('part 1:', part1_result)
print('part 2:', part2_result)
