from pathlib import Path
from dataclasses import dataclass


@dataclass
class Command:
    type: str
    qty: int


@dataclass
class State:
    x: int
    y: int
    aim: int = 0


cmd_functions_part1 = {
    'forward': lambda s, qty: State(s.x + qty, s.y),
    'down': lambda s, qty: State(s.x, s.y + qty),
    'up': lambda s, qty: State(s.x, s.y - qty)
}

cmd_functions_part2 = {
    'forward': lambda s, qty: State(s.x + qty, s.y + s.aim * qty, s.aim),
    'down': lambda s, qty: State(s.x, s.y, s.aim + qty),
    'up': lambda s, qty: State(s.x, s.y, s.aim - qty),
}


def parse_input(filename) -> list[Command]:
    def parse_line(line) -> Command:
        cmd, qty = line.split()
        return Command(cmd, int(qty))

    return [parse_line(line) for line in Path(filename).read_text().splitlines()]


def final_state(commands: list[Command], cmd_functions) -> State:
    state = State(0, 0)
    for cmd in commands:
        state = cmd_functions[cmd.type](state, cmd.qty)
    return state


commands = parse_input('input.txt')
final_pos_part1 = final_state(commands, cmd_functions_part1)
final_pos_part2 = final_state(commands, cmd_functions_part2)

assert final_pos_part1.x * final_pos_part1.y == 1480518
assert final_pos_part2.x * final_pos_part2.y == 1282809906
