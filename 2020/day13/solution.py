import itertools
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Bus:
    dep: int
    offs: int


def parse_buses(line):
    return [
        Bus(int(dep), offset)
        for offset, dep in enumerate(line.split(','))
        if dep != 'x'
    ]


def solve_part1(buses, arrival):
    time_to_wait, earliest_bus = min(
        (bus.dep - (arrival % bus.dep), bus.dep) for bus in buses
    )
    return time_to_wait * earliest_bus


def is_good_time(time, buses):
    return all((time + bus.offs) % bus.dep == 0 for bus in buses)


def solve_part2(buses):
    start = buses[0].dep - buses[0].offs
    interval = 1

    for idx, bus in enumerate(buses):
        for time in itertools.count(start, interval):
            if is_good_time(time, buses[: idx + 1]):
                start = time
                interval *= bus.dep
                break

    return start


lines = Path('input.txt').read_text().splitlines()

arrival = int(lines[0])
buses = parse_buses(lines[1])


assert solve_part1(buses, arrival) == 3464
assert solve_part2(buses) == 760171380521445
