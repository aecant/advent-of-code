import itertools
from collections import defaultdict, deque
from pathlib import Path

import numpy as np


def create_rotations():
    rotations = []
    for x, y, z in itertools.permutations([0, 1, 2]):
        for sx, sy, sz in itertools.product([-1, 1], repeat=3):
            rotation_matrix = np.zeros((3, 3), dtype=int)
            rotation_matrix[0, x] = sx
            rotation_matrix[1, y] = sy
            rotation_matrix[2, z] = sz
            if np.linalg.det(rotation_matrix) == 1:
                rotations.append(rotation_matrix)
    return rotations


rotations = create_rotations()


def parse_input(filename):
    def parse_scanner(scanner_text):
        return np.array(
            [list(map(int, line.split(','))) for line in scanner_text.splitlines()[1:]]
        )

    scanners_text = Path(filename).read_text().split('\n\n')
    return list(map(parse_scanner, scanners_text))


scanners = parse_input('input.txt')


def find_common_specific(scanner1, scanner2):
    coords = defaultdict(list)
    for row1 in scanner1:
        for row2 in scanner2:
            diff_vec = tuple(row2 - row1)
            coords[diff_vec].append(row2)
            if len(coords[diff_vec]) == 12:
                all_tuples = set(map(tuple, scanner2))
                common = set(map(tuple, coords[diff_vec]))
                unique = all_tuples - common
                return np.array(list(unique)) - diff_vec
    return None


def find_other_beacons(scanner1, scanner2):
    for rotation in rotations:
        rotated = scanner2.dot(rotation)
        if (coords := find_common_specific(scanner1, rotated)) is not None:
            return np.vstack((scanner1, coords))


def find_all_beacons(scanners):
    taken = {0}
    beacons = scanners[0]
    while len(taken) < len(scanners):
        for i, scanner in enumerate(scanners):
            if i in taken:
                continue
            if (common := find_other_beacons(beacons, scanner)) is not None:
                beacons = common
                taken.add(i)
    return beacons


# print(len(find_all_beacons(scanners)))
from pprint import pprint
pprint(rotations)

