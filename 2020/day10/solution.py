from pathlib import Path
from collections import defaultdict


def find_previous_jolts(jolt, jolt_set):
    return [jolt - diff for diff in (1, 2, 3) if (jolt - diff) in jolt_set]


def find_next_jolt(jolt, jolt_set):
    for diff in (1, 2, 3):
        if jolt + diff in jolt_set:
            return jolt + diff
    return None


def get_diffs_counter(jolt_set):
    counter = defaultdict(int)
    curr, next_ = 0, find_next_jolt(0, jolt_set)
    while next_:
        diff = next_ - curr
        counter[diff] += 1
        curr, next_ = next_, find_next_jolt(curr, jolt_set)

    return counter


def possible_combinations(last_jolt, jolt_set, cache={}):
    if last_jolt in cache:
        return cache[last_jolt]

    prev_jolts = find_previous_jolts(last_jolt, jolt_set)

    if not prev_jolts:
        res = 1
    else:
        res = sum(possible_combinations(prev, jolt_set, cache) for prev in prev_jolts)

    cache[last_jolt] = res

    return res


jolt_set = set(int(line) for line in Path('input.txt').read_text().splitlines())
last_jolt = max(jolt_set) + 3
jolt_set.update((0, last_jolt))

diffs_counter = get_diffs_counter(jolt_set)

part1 = diffs_counter[1] * diffs_counter[3]
part2 = possible_combinations(last_jolt, jolt_set)

assert part1 == 2470
assert part2 == 1973822685184
