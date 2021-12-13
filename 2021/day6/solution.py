from pathlib import Path


def parse_lanternfishes(filename):
    return [int(val) for val in Path(filename).read_text().split(',')]


def find_lanternfishes(initial_lanternfishes, days):
    lfishes = initial_lanternfishes.copy()
    for day in range(days):
        print(day, len(lfishes))
        for i, lfish in enumerate(lfishes):
            if lfish == 0:
                lfishes[i] = 6
                lfishes.append(9)
            else:
                lfishes[i] -= 1
    return lfishes


init_lfishes = parse_lanternfishes('test_input.txt')
init_lfishes = [1]
print(len(find_lanternfishes(init_lfishes, 100)))
