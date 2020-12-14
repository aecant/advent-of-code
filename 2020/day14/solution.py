import re
import itertools
from functools import reduce
from operator import xor
from pathlib import Path


def create_and_mask(mask_str):
    return int(mask_str.replace('X', '1'), 2)


def create_or_mask(mask_str):
    return int(mask_str.replace('X', '0'), 2)


def create_xor_masks(mask_str):
    float_bits = [2**i for i, char in enumerate(mask_str[::-1]) if char == 'X']

    masks = []

    bit_combinations = itertools.product((0, 1), repeat=len(float_bits))

    for comb in bit_combinations:
        mask = reduce(xor, (bit * is_taken for bit, is_taken in zip(float_bits, comb)))
        masks.append(mask)

    return masks


def parse_mem_write(line):
    match = re.match(r'^mem\[(\d+)] = (\d+)$', line)
    addr, val = map(int, match.groups())
    return addr, val


def execute_program_part1(lines):
    mem = {}
    for line in lines:
        if line[:4] == 'mask':
            mask_str = line.split()[2]
            or_mask = create_or_mask(mask_str)
            and_mask = create_and_mask(mask_str)
        else:
            addr, val = parse_mem_write(line)
            mem[addr] = val & and_mask | or_mask

    return mem


def execute_program_part2(lines):
    mem = {}
    for line in lines:
        if line[:4] == 'mask':
            mask_str = line.split()[2]
            or_mask = create_or_mask(mask_str)
            xor_masks = create_xor_masks(mask_str)
        else:
            addr, val = parse_mem_write(line)
            addr_list = [addr ^ xor_mask | or_mask for xor_mask in xor_masks]
            mem.update(dict.fromkeys(addr_list, val))

    return mem


lines = Path('input.txt').read_text().splitlines()

result_part1 = sum(execute_program_part1(lines).values())
result_part2 = sum(execute_program_part2(lines).values())

print('part 1:', result_part1)
print('part 2:', result_part2)

assert result_part1 == 11612740949946
assert result_part2 == 3394509207186
