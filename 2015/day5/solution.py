from itertools import pairwise, accumulate
from pathlib import Path


def contains_more_non_overlapping_pairs(s):
    pairs_wo_overlap = [p1 for p1, p2 in pairwise(pairwise(s)) if p1 != p2]
    pairs_wo_overlap.append(tuple(s[-2:]))

    return len(pairs_wo_overlap) != len(set(pairs_wo_overlap))


def is_nice_part1(s):
    return (
        any(acc >= 3 for acc in accumulate(s.count(vow) for vow in 'aeiou'))
        and any(c1 == c2 for c1, c2 in pairwise(s))
        and not any(pair in s for pair in ('ab', 'cd', 'pq', 'xy'))
    )


def is_nice_part2(s):
    return contains_more_non_overlapping_pairs(s) and any(
        c1 == c3 for c1, c3 in zip(s, s[2:])
    )


lines = Path('input.txt').read_text().splitlines()

assert sum(map(is_nice_part1, lines)) == 258
assert sum(map(is_nice_part2, lines)) == 53
