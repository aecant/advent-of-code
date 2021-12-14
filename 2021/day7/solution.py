from pathlib import Path
import numpy as np


def parse_crabs(filename):
    return [int(val) for val in Path(filename).read_text().split(',')]


def sum_up_to(num):
    return np.arange(num + 1).sum()


def find_min_fuel(crabs, distance_function):
    def calc_fuel(spot):
        return sum(distance_function(abs(crab - spot)) for crab in crabs)

    def find_minimum(left, right):
        spot = left + (right - left) // 2
        fuel = calc_fuel(spot)
        right_fuel = calc_fuel(spot + 1)
        left_fuel = calc_fuel(spot - 1)

        if fuel <= left_fuel and fuel <= right_fuel:
            return fuel

        if fuel < right_fuel:
            return find_minimum(left, spot)
        else:
            return find_minimum(spot, right)

    return find_minimum(min(crabs), max(crabs))


crabs = parse_crabs('input.txt')

assert find_min_fuel(crabs, lambda d: d) == 342730
assert find_min_fuel(crabs, sum_up_to) == 92335207
