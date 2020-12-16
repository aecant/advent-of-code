import pathlib


def find_addends(numbers, number_set, sum_):
    for num in numbers:
        diff = sum_ - num
        if diff in number_set:
            return num, diff

    return None


def solve_part2(numbers, number_set):
    for num in numbers:
        diff_to_2020 = 2020 - num
        addends = find_addends(numbers, number_set, diff_to_2020)
        if addends:
            return num * addends[0] * addends[1]


numbers = [int(line) for line in pathlib.Path('input.txt').read_text().splitlines()]

number_set = set(numbers)

num1, num2 = find_addends(numbers, number_set, 2020)
result_part1 = num1 * num2

result_part2 = solve_part2(numbers, number_set)

print('part 1:', num1 * num2)
print('part 2:', result_part2)

assert result_part1 == 646779
assert result_part2 == 246191688
