from pathlib import Path


def next_pos(pos, move):
    next_pos_funcs = {
        '^': lambda x, y: (x, y + 1),
        'v': lambda x, y: (x, y - 1),
        '>': lambda x, y: (x + 1, y),
        '<': lambda x, y: (x - 1, y)
    }
    return next_pos_funcs[move](*pos)


def visited_houses_part1(moves):
    init_pos = (0, 0)
    visited = {init_pos}
    pos = init_pos
    for move in moves:
        pos = next_pos(pos, move)
        visited.add(pos)

    return visited


def visited_houses_part2(moves):
    init_pos = (0, 0)
    visited = {init_pos}
    santa_pos = robot_pos = init_pos
    for santa_move, robot_move in zip(moves[::2], moves[1::2]):
        santa_pos = next_pos(santa_pos, santa_move)
        robot_pos = next_pos(robot_pos, robot_move)
        visited.update((santa_pos, robot_pos))

    return visited


moves = Path('input.txt').read_text()

print(len(visited_houses_part1(moves)))
print(len(visited_houses_part2(moves)))
