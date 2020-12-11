from pathlib import Path

DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def dimensions(mat):
    return len(mat), len(mat[0])


def is_ok_pos(pos_i, pos_j, mat):
    rows, cols = dimensions(mat)
    return 0 <= pos_i < rows and 0 <= pos_j < cols


def find_neighbours(pos_i, pos_j, mat):
    for dir_i, dir_j in DIRECTIONS:
        nbr_i, nbr_j = pos_i + dir_i, pos_j + dir_j
        if is_ok_pos(nbr_i, nbr_j, mat):
            yield mat[nbr_i][nbr_j]


def find_visible(pos_i, pos_j, mat):
    for dir_i, dir_j in DIRECTIONS:
        i, j = pos_i + dir_i, pos_j + dir_j
        while is_ok_pos(i, j, mat):
            if mat[i][j] != '.':
                yield mat[i][j]
                break
            i, j = i + dir_i, j + dir_j


def next_state_part1(pos_i, pos_j, mat):
    return next_state(pos_i, pos_j, mat, find_neighbours, 4)


def next_state_part2(pos_i, pos_j, mat):
    return next_state(pos_i, pos_j, mat, find_visible, 5)


def next_state(pos_i, pos_j, mat, find_seats_func, max_occupied):
    val = mat[pos_i][pos_j]

    count_occupied = sum(1 for seat in find_seats_func(pos_i, pos_j, mat) if seat == '#')

    if val == 'L' and count_occupied == 0:
        return '#'
    if val == '#' and count_occupied >= max_occupied:
        return 'L'
    return val


def next_mat(old_mat, next_state_func):
    rows, cols = dimensions(old_mat)
    new_mat = [[' '] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            new_mat[i][j] = next_state_func(i, j, old_mat)

    return new_mat


def next_until_stabilized(mat, next_state_func):
    cur, nxt = mat, next_mat(mat, next_state_func)

    while cur != nxt:
        cur, nxt = nxt, next_mat(nxt, next_state_func)

    return cur


def count_occupied_seats(mat):
    return sum(sum(1 for elem in row if elem == '#') for row in mat)


lines = Path('input.txt').read_text().splitlines()

print('part 1:', count_occupied_seats(next_until_stabilized(lines, next_state_part1)))
print('part 2:', count_occupied_seats(next_until_stabilized(lines, next_state_part2)))
