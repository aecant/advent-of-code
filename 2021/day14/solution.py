from pathlib import Path
from itertools import pairwise
from collections import Counter
from functools import cache


def parse_input(filename):
    def parse_rule(line):
        pair, to_insert = line.split(' -> ')
        return tuple(pair), to_insert

    template, rules_str = Path(filename).read_text().split('\n\n')
    rules = dict(map(parse_rule, rules_str.splitlines()))
    return template, rules


def find_template_counter(template, steps, rules):
    @cache
    def find_pair_counter(pair, step):
        exp = rules[pair]

        if step == 1:
            return Counter(exp)

        return (
            Counter(exp)
            + find_pair_counter((pair[0], exp), step - 1)
            + find_pair_counter((exp, pair[1]), step - 1)
        )

    pair_counters = (find_pair_counter(pair, steps) for pair in pairwise(template))
    return sum(pair_counters, Counter(template))


def get_points(counter):
    most_common = max(counter.values())
    least_common = min(counter.values())
    return most_common - least_common


template, rules = parse_input('input.txt')

counter_part1 = find_template_counter(template, 10, rules)
counter_part2 = find_template_counter(template, 40, rules)

assert get_points(counter_part1) == 3230
assert get_points(counter_part2) == 3542388214529
