import math
from itertools import chain, combinations
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Img:
    tile_id: int
    edges: set[int]
    rev_edges: set[int]
    mat: np.array = field(repr=False)


def parse_image(img_txt):
    lines = img_txt.splitlines()

    tile_id = int(lines[0].split()[1].replace(':', ''))
    mat = np.array([['1' if char == '#' else '0' for char in line] for line in lines[1:]])
    edges, rev_edges = get_edges(mat)

    return Img(tile_id, edges, rev_edges, mat)


def get_edges(mat):
    edges_arr = (mat[0], mat[-1], mat[:, 0], mat[:, -1])  # up, down, left, right
    edges = {int(''.join(edge), 2) for edge in edges_arr}
    rev_edges = {int(''.join(reversed(edge)), 2) for edge in edges_arr}

    return edges, rev_edges


def create_edge_to_id_dict(imgs):
    tile_ids = defaultdict(list)

    for img in imgs:
        for edge in chain(img.edges, img.rev_edges):
            tile_ids[edge].append(img.tile_id)

    return tile_ids


def create_compatibility_dict(edge_to_id_dict):
    compat = defaultdict(set)
    for tile_ids in edge_to_id_dict.values():
        for tile_id1, tile_id2 in combinations(tile_ids, 2):
            compat[tile_id1].add(tile_id2)
            compat[tile_id2].add(tile_id1)
    return compat


def multiply_corners(compatible_dict):
    corners = (tile_id for tile_id, compatible in compatible_dict.items() if len(compatible) == 2)
    return math.prod(corners)


img_txts = Path('input.txt').read_text().split('\n\n')
imgs = list(map(parse_image, img_txts))

edge_to_id_dict = create_edge_to_id_dict(imgs)
compatible_dict = create_compatibility_dict(edge_to_id_dict)


result_part1 = multiply_corners(compatible_dict)

print(result_part1)

# assert result_part1 == 15003787688423
