from pathlib import Path
import re


def validate_hgt(hgt):
    match = re.match(r'(\d+)(cm|in)', hgt)
    if not match:
        return False
    qty, unit = match.groups()
    if unit == 'cm':
        return 150 <= int(qty) <= 193
    else:
        return 50 <= int(qty) <= 76


field_validators = {
    'byr': [str.isdigit, lambda x: 1920 <= int(x) <= 2002],
    'iyr': [str.isdigit, lambda x: 2010 <= int(x) <= 2020],
    'eyr': [str.isdigit, lambda x: 2020 <= int(x) <= 2030],
    'hgt': [validate_hgt],
    'hcl': [re.compile('^#[0-9a-f]{6}$').match],
    'ecl': [lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}],
    'pid': [re.compile('^\d{9}$').match]
}


def parse_passport(s):
    return dict(re.findall(r'(\w{3}):(\S+)', s))


def validate_part1(passport):
    return all(field in passport for field in field_validators)


def validate_part2(passport):
    return all(
        field in passport and all(validator(passport[field]) for validator in validators)
        for field, validators in field_validators.items())


passports = [parse_passport(s) for s in Path('input.txt').read_text().split('\n\n')]

part1_result = sum(1 for passport in passports if validate_part1(passport))
part2_result = sum(1 for passport in passports if validate_part2(passport))

print('part 1:', part1_result)
print('part 2:', part2_result)

