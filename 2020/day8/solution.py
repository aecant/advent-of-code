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
    'nop': lambda state, _: State(state.idx + 1, state.accum)
}


switched_type = {'acc': 'acc', 'jmp': 'nop', 'nop': 'jmp'}


def next_state(state, instr):
    return next_state_functions[instr.type](state, instr)


def next_state_with_switch(state, instr):
    return next_state(state, Instruction(switched_type[instr.type], instr.val))


def parse_instruction(line):
    type_, val = line.split()
    return Instruction(type_, int(val))


def build_reverse_graph(instructions):
    parents = [[] for _ in instructions]
    for idx, instr in enumerate(instructions):
        next_idx = next_state(State(idx), instr).idx
        if next_idx < len(parents):
            parents[next_idx].append(idx)

    return parents


def find_indirect_parents(instr_idx, instructions):
    reverse_graph = build_reverse_graph(instructions)
    queue = reverse_graph[instr_idx]
    visited_nodes = set()
    while queue:
        idx = queue.pop()
        if idx not in visited_nodes:
            visited_nodes.add(idx)
            queue.extend(reverse_graph[idx])

    return visited_nodes


def final_state(instructions, init_state=State()):
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
    final_idxs = find_indirect_parents(last_instr_idx, instructions) | {last_instr_idx}
    state = State()
    while True:
        next_with_switch = next_state_with_switch(state, instructions[state.idx])
        if next_with_switch.idx in final_idxs:
            return final_state(instructions, next_with_switch)
        state = next_state(state, instructions[state.idx])


lines = Path('input.txt').read_text().splitlines()
instructions = list(map(parse_instruction, lines))

result_part1 = final_state(instructions).accum
result_part2 = final_state_with_switch(instructions).accum

assert result_part1 == 1859
assert result_part2 == 1235
