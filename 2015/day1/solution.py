from pathlib import Path


floor_change = {
    '(': 1,
    ')': -1
}


def solve_part1(parentheses):
    return sum(floor_change[paren] for paren in parentheses)


def solve_part2(parentheses):
    floor = 0
    for pos, paren in enumerate(parentheses):
        floor += floor_change[paren]
        if floor == -1:
            return pos + 1


parentheses = Path('input.txt').read_text()

print(solve_part1(parentheses))
print(solve_part2(parentheses))
