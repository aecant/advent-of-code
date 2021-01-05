from __future__ import annotations

import math
from itertools import chain, combinations
from collections import defaultdict, deque
from pathlib import Path
from dataclasses import dataclass, field, replace

import numpy as np

monster = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]])

transforms_list = [(),
                   (np.rot90,),
                   (np.fliplr,),
                   (np.flipud,),
                   (np.rot90, np.fliplr),
                   (np.rot90, np.flipud),
                   (np.fliplr, np.flipud),
                   (np.rot90, np.fliplr, np.flipud)]


@dataclass
class Tile:
    id: int
    mat: np.array
    borders: set[int]
    rev_borders: set[int]
    pos: tuple[int, int] = None
    adj: set[Tile] = field(default_factory=set)

    def __repr__(self):
        return f't{self.id}'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


def tuple_diff(t1, t2):
    return tuple(e1 - e2 for e1, e2 in zip(t1, t2))


def parse_tiles(img_txts):
    tiles = dict(map(parse_tile, img_txts))
    add_adjacency(tiles)
    add_positions(tiles)
    return tiles


def parse_tile(img_txt):
    lines = img_txt.splitlines()

    tile_id = int(lines[0].split()[1].replace(':', ''))
    mat = np.array([[1 if char == '#' else 0 for char in line] for line in lines[1:]])

    borders_array = (mat[0], mat[-1], mat[:, 0], mat[:, -1])  # up, down, left, right
    borders = {int(''.join(map(str, border)), 2) for border in borders_array}
    rev_borders = {int(''.join(map(str, reversed(border))), 2) for border in borders_array}

    return tile_id, Tile(tile_id, mat, borders, rev_borders)


def create_border_to_tile_dict(tiles):
    border_to_tile = defaultdict(list)

    for tile in tiles.values():
        for border in chain(tile.borders, tile.rev_borders):
            border_to_tile[border].append(tile)

    return border_to_tile


def add_adjacency(tiles):
    border_to_tile = create_border_to_tile_dict(tiles)
    for adjacent_tiles in border_to_tile.values():
        for tile1, tile2 in combinations(adjacent_tiles, 2):
            tile1.adj.add(tile2)
            tile2.adj.add(tile1)


def get_corners(tiles):
    return (tile for tile in tiles.values() if len(tile.adj) == 2)


def neighbors(mat, idxs):
    def is_valid(idxs, dim):
        i, j = idxs
        return 0 <= i < dim and 0 <= j < dim

    nbr_idxs_list = np.array(((0, 1), (1, 0), (-1, 0), (0, -1)))
    return [mat[tuple(idxs + nbr_idxs)] for nbr_idxs in nbr_idxs_list
            if is_valid(idxs + nbr_idxs, mat.shape[0])]


def add_positions(tiles):
    def find_correct_tile(nbrs, taken):
        empty_nbrs_count = sum(1 for nbr in nbrs if nbr is None)
        for nbr in filter(bool, nbrs):
            for adj in nbr.adj - taken:
                avail_adj = adj.adj - taken
                if len(avail_adj) == empty_nbrs_count:
                    return adj

    shape = (int(math.sqrt(len(tiles))), ) * 2
    pos_mat = np.empty(shape, Tile)

    up_left_corner = next(get_corners(tiles))
    up_left_corner.pos = (0, 0)
    pos_mat[0, 0] = up_left_corner
    taken = {up_left_corner}

    for idxs in np.ndindex(shape):
        if pos_mat[idxs] in taken:
            continue
        nbrs = neighbors(pos_mat, idxs)

        tile = find_correct_tile(nbrs, taken)
        tile.pos = idxs
        pos_mat[idxs] = tile
        taken.add(tile)


def has_aligned_border(tile1, tile2):
    idxs_dict = {
        (0, -1): ((..., -1), (..., 0)),
        (0, 1): ((..., 0), (..., -1)),
        (-1, 0): ((-1, ...), (0, ...)),
        (1, 0): ((0, ...), (-1, ...))
    }
    diff = tuple_diff(tile1.pos, tile2.pos)
    idxs1, idxs2 = idxs_dict[diff]
    return np.array_equal(tile1.mat[idxs1], tile2.mat[idxs2])


def reject_candidate(chosen_tiles):
    return any(not has_aligned_border(t1, t2)
               for t1, t2 in combinations(chosen_tiles, 2) if t2 in t1.adj)


def apply_transforms(mat, transforms):
    for trans in transforms:
        mat = trans(mat)
    return mat


def get_mat_transforms(mat):
    return (apply_transforms(mat, transforms) for transforms in transforms_list)


def get_tile_transforms(tile):
    return (replace(tile, mat=mat) for mat in get_mat_transforms(tile.mat))


def get_ordered_tiles(first):
    tiles = []
    added = set()
    queue = deque((first,))
    while queue:
        tile = queue.pop()
        if tile not in added:
            tiles.append(tile)
            added.add(tile)
            queue.extendleft(tile.adj - added)
    return tiles


def backtrack(ord_tiles, candidate):
    if reject_candidate(candidate):
        return None
    if len(candidate) == len(ord_tiles):
        return candidate

    ord_tile_idx = len(candidate)
    tile_transforms = get_tile_transforms(ord_tiles[ord_tile_idx])
    for transform in tile_transforms:
        next_candidate = candidate | {transform}
        if solution := backtrack(ord_tiles, next_candidate):
            return solution

    return None


def find_correct_tile_transform(tiles):
    up_left = next(tile for tile in tiles.values() if tile.pos == (0, 0))
    ord_tiles = get_ordered_tiles(up_left)
    return backtrack(ord_tiles, set())


def rebuild_image(tiles):
    arranged_tiles = find_correct_tile_transform(tiles)
    shape = (int(math.sqrt(len(tiles))), ) * 2
    mat_pos = np.empty(shape, Tile)
    for tile in arranged_tiles:
        mat_pos[tile.pos] = tile

    return np.vstack(
        [np.hstack([tile.mat[1:-1, 1:-1] for tile in row])
         for row in mat_pos]
    )


def get_monster_positions(img):
    height, width = monster.shape
    return [(i, j) for i, j in np.ndindex(tuple_diff(img.shape, monster.shape))
            if (monster | img[i: i + height, j: j + width]).all()]


def get_water_roughness(img):
    height, width = monster.shape
    for transf_img in get_mat_transforms(img):
        if monster_positions := get_monster_positions(transf_img):
            for i, j in monster_positions:
                transf_img[i: i + height, j: j + width] *= monster
            return transf_img.sum()


img_txts = Path('input.txt').read_text().split('\n\n')

tiles = parse_tiles(img_txts)
img = rebuild_image(tiles)

result_part1 = math.prod(tile.id for tile in get_corners(tiles))
result_part2 = get_water_roughness(img)

print(result_part1)
print(result_part2)

assert result_part1 == 15003787688423
assert result_part2 == 1705
