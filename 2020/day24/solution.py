from itertools import chain
from pathlib import Path
from functools import cache

next_pos_funcs = {
    'ne': lambda x, y: (x + 1 - y % 2, y + 1),
    'nw': lambda x, y: (x - y % 2, y + 1),
    'se': lambda x, y: (x + 1 - y % 2, y - 1),
    'sw': lambda x, y: (x - y % 2, y - 1),
    'w': lambda x, y: (x - 1, y),
    'e': lambda x, y: (x + 1, y),
}


def parse_directions(line):
    dirs = []
    i = 0
    while i < len(line):
        jump = 1 if line[i] in ('w', 'e') else 2
        dirs.append(line[i : i + jump])
        i += jump
    return dirs


def get_tile_to_flip(dirs):
    x, y = 0, 0
    for dir_ in dirs:
        x, y = next_pos_funcs[dir_](x, y)
    return x, y


def get_initial_black_tiles(dirs_list):
    black_tiles = set()
    for dirs in dirs_list:
        flip_tile = get_tile_to_flip(dirs)
        if flip_tile in black_tiles:
            black_tiles.remove(flip_tile)
        else:
            black_tiles.add(flip_tile)
    return black_tiles


def get_neighbors(tile):
    return (next_pos_func(*tile) for next_pos_func in next_pos_funcs.values())


def get_next_day_black_tiles(black_tiles):
    @cache
    def is_next_color_black(tile):
        black_nbrs = sum(nbr in black_tiles for nbr in get_neighbors(tile))
        if tile in black_tiles:
            return black_nbrs in (1, 2)
        return black_nbrs == 2

    next_black_tiles = set()
    for black_tile in black_tiles:
        for tile in chain([black_tile], get_neighbors(black_tile)):
            if is_next_color_black(tile):
                next_black_tiles.add(tile)
    return next_black_tiles


def get_black_tiles_after_100_days(init_black_tiles):
    black_tiles = init_black_tiles
    for _ in range(100):
        black_tiles = get_next_day_black_tiles(black_tiles)
    return black_tiles


lines = Path('input.txt').read_text().splitlines()
dirs_list = list(map(parse_directions, lines))

init_black_tiles = get_initial_black_tiles(dirs_list)

result_part1 = len(init_black_tiles)
result_part2 = len(get_black_tiles_after_100_days(init_black_tiles))

assert result_part1 == 465
assert result_part2 == 4078
