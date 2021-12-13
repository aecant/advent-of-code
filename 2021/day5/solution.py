import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(order=True)
class Point:
    x: int
    y: int


def parse_vents(filename):
    def parse_vent(line):
        x1, y1, x2, y2 = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line).groups()
        return Point(int(x1), int(y1)), Point(int(x2), int(y2))

    return [parse_vent(line) for line in Path(filename).read_text().splitlines()]


def trace_vents(vents, ignore_diagonals):
    matrix = init_matrix(vents)
    for v1, v2 in vents:
        orig = min(v1, v2)
        dest = max(v1, v2)

        is_diagonal = orig.x != dest.x and orig.y != dest.y
        if is_diagonal:
            if ignore_diagonals:
                continue

            submatrix_dim = dest.x - orig.x + 1
            if orig.y > dest.y:
                eye = np.rot90(np.eye(submatrix_dim))
                matrix[orig.x : dest.x + 1, dest.y : orig.y + 1] += eye
            else:
                eye = np.eye(submatrix_dim)
                matrix[orig.x : dest.x + 1, orig.y : dest.y + 1] += eye

        else:
            matrix[orig.x : dest.x + 1, orig.y : dest.y + 1] += 1

    return matrix


def init_matrix(vents):
    dim = 1 + max(max(orig.x, orig.y, dest.x, dest.y) for orig, dest in vents)
    return np.zeros((dim, dim))


vents = parse_vents('input.txt')
matrix_part1 = trace_vents(vents, ignore_diagonals=True)
matrix_part2 = trace_vents(vents, ignore_diagonals=False)
assert (matrix_part1 >= 2).sum() == 4655
assert (matrix_part2 >= 2).sum() == 20500
