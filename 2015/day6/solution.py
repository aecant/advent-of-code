import re
from pathlib import Path

import numpy as np

DIM = 1000


functions_part1 = {
    'turn on': lambda x: 1,
    'turn off': lambda x: 0,
    'toggle': lambda x: x ^ 1
}

functions_part2 = {
    'turn on': lambda x: x + 1,
    'turn off': lambda x: (x - 1).clip(0),
    'toggle': lambda x: x + 2
}


def parse_transform(line):
    instr = re.match(r'^(\D+) ', line).group(1)
    i1, j1, i2, j2 = map(int, re.findall(r'\d+', line))

    return instr, i1, i2 + 1, j1, j2 + 1


def apply_transformations(transforms, functions):
    grid = np.zeros((DIM, DIM), int)
    for instr, i1, i2, j1, j2 in transforms:
        grid[i1:i2, j1:j2] = functions[instr](grid[i1:i2, j1:j2])

    return grid


lines = Path('input.txt').read_text().splitlines()
transforms = list(map(parse_transform, lines))


result_part1 = apply_transformations(transforms, functions_part1).sum()
result_part2 = apply_transformations(transforms, functions_part2).sum()

print(result_part1)
print(result_part2)

assert result_part1 == 569999
assert result_part2 == 17836115
