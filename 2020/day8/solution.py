from pathlib import Path
from dataclasses import dataclass


@dataclass
class Instruction:
    type: str
    val: int


@dataclass
class State:
    idx: int = 0  # instruction index
    accum: int = 0


next_state_functions = {
    'acc': lambda state, instr: State(state.idx + 1, state.accum + instr.val),
    'jmp': lambda state, instr: State(state.idx + instr.val, state.accum),
    'nop': lambda state, instr: State(state.idx + 1, state.accum)
}


switched_type = {'acc': 'acc', 'jmp': 'nop', 'nop': 'jmp'}


def next_state(state, instr):
    return next_state_functions[instr.type](state, instr)


def next_state_with_switch(state, instr):
    return next_state(state, Instruction(switched_type[instr.type], instr.val))


def parse_instruction(line):
    type_, val = line.split()
    return Instruction(type_, int(val))


def get_all_direct_parents(instructions):
    parents = [[] for _ in instructions]
    for idx, instr in enumerate(instructions):
        next_idx = next_state(State(idx), instr).idx
        if next_idx < len(parents):
            parents[next_idx].append(idx)

    return parents


def get_indirect_parents(instr_idx, instructions):
    all_direct_parents = get_all_direct_parents(instructions)
    queue = all_direct_parents[instr_idx]
    visited_nodes = set()
    while queue:
        idx = queue.pop()
        if idx not in visited_nodes:
            visited_nodes.add(idx)
            queue.extend(all_direct_parents[idx])

    return visited_nodes


def get_final_state(instructions, init_state=State()):
    seen_instr = set()
    state = init_state
    while state.idx < len(instructions):
        if state.idx in seen_instr:
            return state
        seen_instr.add(state.idx)
        state = next_state(state, instructions[state.idx])

    return state


def final_state_with_switch(instructions):
    last_instr_idx = len(instructions) - 1
    final_idxs = get_indirect_parents(last_instr_idx, instructions) | {last_instr_idx}
    state = State()
    while True:
        next_with_switch = next_state_with_switch(state, instructions[state.idx])
        if next_with_switch.idx in final_idxs:
            return get_final_state(instructions,next_with_switch)
        state = next_state(state, instructions[state.idx])


lines = Path('input.txt').read_text().splitlines()
instructions = list(map(parse_instruction, lines))

print('part 1:', get_final_state(instructions).accum)
print('part 2:', final_state_with_switch(instructions).accum)
