from dataclasses import dataclass
from itertools import count


@dataclass
class Packet:
    version: int
    type: int
    literal: int | None


def hex_to_bin(hex):
    return f"{int(hex, 16):b}"


def bin_to_dec(bin):
    return int(bin, 2)


def parse_literal(bits):
    literal_bits = []
    for cur in count(0, 5):
        literal_bits += bits[cur + 1 : cur + 5]
        if bits[cur] == "0":
            break
    literal = bin_to_dec("".join(literal_bits))
    return literal, cur


def parse_packet(bits):
    version = bin_to_dec(bits[:3])
    type = bin_to_dec(bits[3:6])
    if type == 4:
        literal, cur = parse_literal(bits[6:])

    return Packet(version, type, literal), cur


packet, _ = parse_packet("110100101111111000101000")
assert packet.literal == 2021
assert packet.version == 6
assert packet.type == 4
