from pathlib import Path


def bin_search(sequence, first_half_char):
    left = 0
    right = 2**len(sequence)

    for char in sequence:
        if char == first_half_char:
            right -= (right - left) // 2
        else:
            left += (right - left) // 2

    return left


def get_seat_id(ticket):
    row = bin_search(ticket[:-3], 'F')
    col = bin_search(ticket[-3:], 'L')
    return row * 8 + col


def get_my_seat_id(ids):
    return next(cur + 1 for cur, nxt in zip(ids, ids[1:]) if cur + 1 != nxt)


lines = Path('input.txt').read_text().splitlines()
seat_ids = sorted(map(get_seat_id, lines))

part1_result = seat_ids[-1]
part2_result = get_my_seat_id(seat_ids)

print('part1:', part1_result)
print('part2:', part2_result)

assert part1_result == 994
assert part2_result == 741
