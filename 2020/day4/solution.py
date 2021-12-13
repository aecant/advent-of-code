from pathlib import Path
import re


def validate_hgt(hgt):
    match = re.match(r'(\d+)(cm|in)', hgt)
    if not match:
        return False

    qty, unit = match.groups()

    if unit == 'cm':
        return 150 <= int(qty) <= 193

    return 50 <= int(qty) <= 76


validators = {
    'byr': lambda s: str.isdigit and 1920 <= int(s) <= 2002,
    'iyr': lambda s: str.isdigit and 2010 <= int(s) <= 2020,
    'eyr': lambda s: str.isdigit and 2020 <= int(s) <= 2030,
    'hgt': validate_hgt,
    'hcl': re.compile(r'^#[0-9a-f]{6}$').match,
    'ecl': lambda s: s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': re.compile(r'^\d{9}$').match
}


def parse_passport(s):
    return dict(re.findall(r'(\w{3}):(\S+)', s))


def validate_part1(passport):
    return all(field in passport for field in validators)


def validate_part2(passport):
    return all(field in passport and is_valid(passport[field]) for field, is_valid in validators.items())


passports = [parse_passport(s) for s in Path('input.txt').read_text().split('\n\n')]


part1_result = sum(map(validate_part1, passports))
part2_result = sum(map(validate_part2, passports))

assert part1_result == 219
assert part2_result == 127
