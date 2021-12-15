from heapq import heappop, heappush
from pathlib import Path

import numpy as np


def parse_risk_matrix(filename):
    lines = Path(filename).read_text().splitlines()
    return np.array([np.fromiter(line, dtype=int) for line in lines])


def neighbors(coord, dim):
    i, j = coord
    if i > 0:
        yield i - 1, j
    if i < dim - 1:
        yield i + 1, j
    if j > 0:
        yield i, j - 1
    if j < dim - 1:
        yield i, j + 1


def create_complete_mat(tile):
    def increase_risk(n):
        return (n - 1 + tile) % 9 + 1

    dim = len(tile)
    complete = np.zeros((dim * 5, dim * 5), dtype=int)

    for i in range(5):
        for j in range(5):
            increased = increase_risk(i + j)
            complete[i * dim : i * dim + dim, j * dim : j * dim + dim] = increased

    return complete


def find_min_risk(risk_matrix):
    dim = len(risk_matrix)
    coord_risks = np.full_like(risk_matrix, np.iinfo(risk_matrix.dtype).max)
    queue = [(0, (0, 0))]

    while queue:
        node_risk, node = heappop(queue)
        for nbr in neighbors(node, dim):
            nbr_risk = node_risk + risk_matrix[nbr]
            if nbr_risk < coord_risks[nbr]:
                coord_risks[nbr] = nbr_risk
                heappush(queue, (nbr_risk, nbr))

    return coord_risks[dim - 1, dim - 1]


risk_mat = parse_risk_matrix('input.txt')

print(find_min_risk(risk_mat))
print(find_min_risk(create_complete_mat(risk_mat)))
# assert find_min_risk(risk_mat) == 739
# assert find_min_risk(create_complete_mat(risk_mat)) == 3040
