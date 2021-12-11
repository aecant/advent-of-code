from pathlib import Path
from functools import reduce
from dataclasses import dataclass


@dataclass
class Command:
    type: str
    qty: int


@dataclass
class Pos:
    x: int
    y: int


cmd_functions = {
    'forward': lambda pos, qty: Pos(pos.x + qty, pos.y),
    'down': lambda pos, qty: Pos(pos.x, pos.y + qty),
    'up': lambda pos, qty: Pos(pos.x, pos.y - qty)
}


def parse_input(filename) -> list[Command]:
    def parse_line(line) -> Command:
        cmd, qty = line.split()
        return Command(cmd, int(qty))

    return [parse_line(line) for line in Path(filename).read_text().splitlines()]


def next_pos(pos: Pos, cmd: Command) -> Pos:
    return cmd_functions[cmd.type](pos, cmd.qty)


def final_position(commands: list[Command]) -> Pos:
    pos = Pos(0, 0)
    for cmd in commands:
        pos = next_pos(pos, cmd)
    return pos


commands = parse_input('input.txt')
final_pos = final_position(commands)
assert final_pos.x * final_pos.y == 1480518
