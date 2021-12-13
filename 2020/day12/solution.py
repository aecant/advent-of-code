from pathlib import Path
from dataclasses import dataclass

import numpy as np


rot_mat = {
    90: np.array(((0, -1), (1, 0))),
    180: np.array(((-1, 0), (0, -1))),
    270: np.array(((0, 1), (-1, 0))),
}

dir_vec = {
    'N': np.array((0, 1)),
    'S': np.array((0, -1)),
    'E': np.array((1, 0)),
    'W': np.array((-1, 0)),
}

next_state_funcs_part1 = {
    **dict.fromkeys(
        ['N', 'S', 'E', 'W'], lambda s, i: State(s.pos + dir_vec[i.typ] * i.val, s.dir)
    ),
    'F': lambda s, i: State(s.pos + s.dir * i.val, s.dir),
    'L': lambda s, i: State(s.pos, rot_mat[i.val].dot(s.dir)),
    'R': lambda s, i: State(s.pos, s.dir.dot(rot_mat[i.val])),
}

next_state_funcs_part2 = {
    **next_state_funcs_part1,
    **dict.fromkeys(
        ['N', 'S', 'E', 'W'], lambda s, i: State(s.pos, s.dir + dir_vec[i.typ] * i.val)
    ),
}


@dataclass
class State:
    pos: np.array
    dir: np.array


@dataclass
class Instr:
    typ: str
    val: int


def parse_instr(line):
    typ = line[0]
    val = int(line[1:])
    return Instr(typ, val)


def get_last_state(instructions, init_dir, next_state_funcs):
    state = State(np.array((0, 0)), init_dir)
    for instr in instructions:
        state = next_state_funcs[instr.typ](state, instr)
    return state


lines = Path('input.txt').read_text().splitlines()
instructions = list(map(parse_instr, lines))

last_state_part1 = get_last_state(instructions, dir_vec['E'], next_state_funcs_part1)
last_state_part2 = get_last_state(
    instructions, np.array((10, 1)), next_state_funcs_part2
)

assert np.abs(last_state_part1.pos).sum() == 439
assert np.abs(last_state_part2.pos).sum() == 12385
