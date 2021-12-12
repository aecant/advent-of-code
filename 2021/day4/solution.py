from pathlib import Path
import numpy as np


class Board:
    def __init__(self, matrix):
        self._matrix = matrix.copy()
        self._dim = len(matrix)
        self._pos_idx = {val: pos for pos, val in np.ndenumerate(matrix)}
        self._marked_by_row = [0] * self._dim
        self._marked_by_col = [0] * self._dim
        self.won = False

    def mark_and_check_win(self, num):
        if num not in self._pos_idx:
            return False
        row, col = self._pos_idx[num]
        self._matrix[row][col] = 0
        if self._mark(self._marked_by_row, row) or self._mark(self._marked_by_col, col):
            return True

        return False

    def _mark(self, arr, idx):
        arr[idx] += 1
        if arr[idx] >= self._dim:
            self.won = True
            return True

    def unmarked_sum(self):
        return self._matrix.sum()


def parse_input(filename):
    drawed_nums_line, *board_raw_strings = Path(filename).read_text().split('\n\n')

    drawed_nums = [int(val) for val in drawed_nums_line.split(',')]

    board_strings = (board.splitlines() for board in board_raw_strings)
    board_matrices = (
        np.array([np.fromiter(row.split(), dtype=int) for row in board])
        for board in board_strings
    )

    boards = [Board(matrix) for matrix in board_matrices]

    return drawed_nums, boards


def find_first_and_last_winning_boards(drawed_nums, boards):
    first = None
    for num in drawed_nums:
        for board in boards:
            if board.won:
                continue
            is_winning = board.mark_and_check_win(num)
            if is_winning:
                last = board.unmarked_sum() * num
                if not first:
                    first = last

    return first, last


drawed_nums, boards = parse_input('input.txt')
first, last = find_first_and_last_winning_boards(drawed_nums, boards)

assert first == 12796
assert last == 18063
