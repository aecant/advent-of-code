from pathlib import Path
from functools import cache


def find_next_jolt(jolt, jolt_set):
    for diff in (1, 2, 3):
        if jolt + diff in jolt_set:
            return jolt + diff


def get_diffs_count(jolt_set):
    count = [0] * len(jolt_set)
    cur, nxt = 0, find_next_jolt(0, jolt_set)
    while nxt:
        diff = nxt - cur
        count[diff] += 1
        cur, nxt = nxt, find_next_jolt(cur, jolt_set)

    return count


def solve_part2(last_jolt, jolt_set):
    def find_previous_jolts(jolt):
        return [jolt - diff for diff in (1, 2, 3) if jolt - diff in jolt_set]

    @cache
    def possible_combinations(last_jolt):
        if prev_jolts := find_previous_jolts(last_jolt):
            return sum(possible_combinations(jolt) for jolt in prev_jolts)
        return 1

    return possible_combinations(last_jolt)


jolt_set = set(int(line) for line in Path('input.txt').read_text().splitlines())
last_jolt = max(jolt_set) + 3
jolt_set.update((0, last_jolt))

diffs_count = get_diffs_count(jolt_set)

part1 = diffs_count[1] * diffs_count[3]
part2 = solve_part2(last_jolt, jolt_set)

assert part1 == 2470
assert part2 == 1973822685184
