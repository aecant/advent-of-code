from pathlib import Path
from dataclasses import dataclass

@dataclass
class PasswordWithPolicy:
    password: str
    policy_char: str
    first_num: int
    second_num: int


def parse_password_with_policy(line: str) -> PasswordWithPolicy:
    split_line = line.split()
    first_num, second_num = (int(num) for num in split_line[0].split('-'))
    policy_char = split_line[1].split(':')[0]
    password = split_line[2]
    return PasswordWithPolicy(password, policy_char, first_num, second_num)


def is_valid_part1(pwp: PasswordWithPolicy) -> bool:
    occurrences = pwp.password.count(pwp.policy_char)
    return pwp.first_num <= occurrences <= pwp.second_num


def is_valid_part2(pwp: PasswordWithPolicy) -> bool:
    policy_char_in_pos1 = pwp.policy_char == pwp.password[pwp.first_num - 1]
    policy_char_in_pos2 = pwp.policy_char == pwp.password[pwp.second_num - 1]
    return policy_char_in_pos1 ^ policy_char_in_pos2


lines = Path('input.txt').read_text().splitlines()

part1_count = sum(1 for line in lines if is_valid_part1(parse_password_with_policy(line)))
part2_count = sum(1 for line in lines if is_valid_part2(parse_password_with_policy(line)))

print('part 1:', part1_count)
print('part 2:', part2_count)
