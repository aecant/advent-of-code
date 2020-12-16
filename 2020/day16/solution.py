import re
import math
from itertools import chain
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass


MAX_FIELD = 1000


Field = namedtuple('Field', ['r1', 'r2', 'name'])
Range = namedtuple('Range', ['min', 'max'])


def create_valid_fields(fields):
    valid_fields = [False] * MAX_FIELD
    for field in fields:
        for r in (field.r1, field.r2):
            valid_fields[r.min: r.max] = [True] * (r.max - r.min)

    return valid_fields


def parse_all_nums(txt):
    return list(map(int, re.findall(r'\d+', txt)))


def parse_field_line(line):
    min1, max1, min2, max2 = parse_all_nums(line)
    name = line.split(':')[0]
    return Field(Range(min1, max1), Range(min2, max2), name)


def parse_fields(text):
    return list(map(parse_field_line, text.splitlines()))


def parse_tickets(text):
    return list(map(parse_all_nums, text.splitlines()[1:]))


def is_valid(value, field):
    return field.r1.min <= value <= field.r1.max or field.r2.min <= value <= field.r2.max


def create_available_fields_for_pos(fields, tickets):
    available = [
        [f for f in fields if all(is_valid(t[pos], f) for t in tickets)]
        for pos, _ in enumerate(fields)
    ]

    return available


def create_field_positions(fields, tickets):
    valid_tickets = [t for t in tickets if all(valid_fields[f] for f in t)]
    available_fields = create_available_fields_for_pos(fields, valid_tickets)
    positions = {}
    picked = set()

    for pos, available in sorted(enumerate(available_fields), key=lambda t: len(t[1])):
        field = next(field for field in available if field not in picked)
        picked.add(field)
        positions[field] = pos

    return positions


def solve_part1(tickets, valid_fields):
    return sum(field for field in chain.from_iterable(tickets) if not valid_fields[field])


def solve_part2(field_pos, my_ticket):
    return math.prod(my_ticket[pos] for field, pos in field_pos.items() if field.name.startswith('departure'))


fields_text, my_ticket_text, nearby_tickets_text = Path('input.txt').read_text().split('\n\n')

fields = parse_fields(fields_text)
my_ticket = parse_all_nums(my_ticket_text)
tickets = parse_tickets(nearby_tickets_text)

valid_fields = create_valid_fields(fields)
field_positions = create_field_positions(fields, tickets)

result_part1 = solve_part1(tickets, valid_fields)
result_part2 = solve_part2(field_positions, my_ticket)

print(result_part1)
print(result_part2)

assert result_part1 == 25972
assert result_part2 == 622670335901
