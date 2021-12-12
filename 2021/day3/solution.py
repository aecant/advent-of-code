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
    gamma_bool_array = columns_sum > num_rows / 2
    gamma_int_array = gamma_bool_array.astype(int)
    gamma = bin_array_to_int(gamma_int_array)
    epsilon = bin_array_to_int(gamma_int_array ^ 1)
    return gamma * epsilon

    


matrix = parse_matrix('input.txt')
print(solve_part1(matrix))
