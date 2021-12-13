from pathlib import Path
from itertools import product

import numpy as np


def indices_valid(shape, indices):
    return all(0 <= idx < max_idx for max_idx, idx in zip(shape, indices))


def get_relative_neighbors(n_dim):
    return np.array(
        [coord for coord in product((-1, 0, 1), repeat=n_dim) if coord != (0,) * n_dim]
    )


def parse_init_mat(lines, n_dim):
    init = np.zeros((len(lines),) * n_dim, int)
    face = np.array([[1 if char == '#' else 0 for char in line] for line in lines], int)
    face_idx = (1,) * (n_dim - 2)
    init[face_idx] = face

    return init


def next_mat(mat, relative_neighbors):
    mat = np.pad(mat, 1)
    nxt = np.zeros(mat.shape, int)

    for indices in np.array(list(np.ndindex(mat.shape))):
        active_neighbors = sum(
            mat[tuple(indices + neighbor)]
            for neighbor in relative_neighbors
            if indices_valid(mat.shape, indices + neighbor)
        )

        if active_neighbors == 3 or mat[tuple(indices)] and active_neighbors == 2:
            nxt[tuple(indices)] = 1

    return nxt


def calculate_mat_after_cycles(init_mat, cycles):
    relative_neighbors = get_relative_neighbors(len(init_mat.shape))
    mat = init_mat
    for _ in range(cycles):
        mat = next_mat(mat, relative_neighbors)
    return mat


lines = Path('input.txt').read_text().splitlines()

init_mat_3d = parse_init_mat(lines, 3)
init_mat_4d = parse_init_mat(lines, 4)


result_part1 = calculate_mat_after_cycles(init_mat_3d, 6).sum()
result_part2 = calculate_mat_after_cycles(init_mat_4d, 6).sum()


assert result_part1 == 315
assert result_part2 == 1520
