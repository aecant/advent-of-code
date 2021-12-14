from pathlib import Path
import numpy as np


def parse_crabs(filename):
    return [int(val) for val in Path(filename).read_text().split(',')]


def sum_up_to(num):
    return np.arange(num + 1).sum()


def calculate_fuel(crabs, distance_function):
    def calculate_spot_fuel(spot):
        return sum(distance_function(abs(crab - spot)) for crab in crabs)

    min_, max_ = min(crabs), max(crabs)
    return map(calculate_spot_fuel, range(min_, max_ + 1))


crabs = parse_crabs('input.txt')

assert min(calculate_fuel(crabs, lambda d: d)) == 342730
assert min(calculate_fuel(crabs, sum_up_to)) == 92335207
