from pathlib import Path
import itertools


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def triplewise(iterable):
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def parse_depths(filename):
    return [int(line) for line in Path(filename).read_text().splitlines()]


def count_increased_part1(depths):
    return sum(e2 > e1 for (e1, e2) in pairwise(depths))


def count_increased_part2(depths):
    return sum(sum(t2) > sum(t1) for (t1, t2) in pairwise(triplewise(depths)))


depths = parse_depths('input.txt')

assert count_increased_part1(depths) == 1298
assert count_increased_part2(depths) == 1248
