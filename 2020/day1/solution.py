import pathlib

numbers = [int(line) for line in pathlib.Path('input.txt').read_text().splitlines()]

number_set = set(numbers)

def find_addends(numbers, number_set, sum_):
    for num in numbers:
        diff = sum_ - num
        if diff in number_set:
            return num, diff

    return None

num1, num2 = find_addends(numbers, number_set, 2020)
print('part 1:', num1 * num2)

for num in numbers:
    diff_to_2020 = 2020 - num
    addends = find_addends(numbers, number_set, diff_to_2020)
    if addends:
        result = num * addends[0] * addends [1]
        print('part 2:', result)
        break

