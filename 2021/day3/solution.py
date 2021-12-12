import itertools
import operator
from pathlib import Path

import numpy as np


def parse_matrix(filename):
    lines = Path(filename).read_text().splitlines()
    return np.array([np.fromiter(line, dtype=int) for line in lines])


def bin_array_to_int(arr):
    string = ''.join(arr.astype(str))
    return int(string, 2)


def solve_part1(matrix):
    columns_sum = matrix.sum(axis=0)
    num_rows = matrix.shape[0]
    most_common_bits = columns_sum > num_rows / 2
    gamma = bin_array_to_int(most_common_bits.astype(int))
    epsilon = bin_array_to_int(most_common_bits ^ 1)
    return gamma * epsilon


def find_rating(matrix, op):
    matrix = matrix.copy()
    for col_idx in itertools.count():
        num_rows = matrix.shape[0]
        col = matrix[:, col_idx]
        bit_criteria = op(col.sum(), num_rows / 2)
        matrix = np.array([row for row in matrix if row[col_idx] == bit_criteria])
        if len(matrix) == 1:
            return bin_array_to_int(matrix[0])


def solve_part2(matrix):
    oxygen = find_rating(matrix, operator.ge)
    co2 = find_rating(matrix, operator.lt)
    return oxygen * co2


matrix = parse_matrix('input.txt')

assert solve_part1(matrix) == 1092896
assert solve_part2(matrix) == 4672151
