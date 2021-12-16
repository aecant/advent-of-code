from __future__ import annotations
import math
from dataclasses import dataclass
from itertools import count
from pathlib import Path

VERS = 3
TYPE = 3
HEAD = VERS + TYPE
LIT_GROUP = 5
OP_BITS = 16
OP_PKT = 12


@dataclass
class Packet:
    version: int
    type: int
    payload: int | list[Packet]
    len: int

    def is_literal(self):
        return isinstance(self.payload, int)


operators = [
    sum,
    math.prod,
    min,
    max,
    None,
    lambda it: next(it) > next(it),
    lambda it: next(it) < next(it),
    lambda it: next(it) == next(it),
]


def parse_input(filename):
    return parse_packet(hex_to_bin(Path(filename).read_text()))


def hex_to_bin(hex):
    padded_len = len(hex) * 4
    return f'{int(hex, 16):0{padded_len}b}'


def bin_to_dec(bin):
    return int(bin, 2)


def parse_packet(bits):
    version = bin_to_dec(bits[:VERS])
    type = bin_to_dec(bits[VERS:HEAD])
    if type == 4:
        return parse_literal(bits[HEAD:], version, type)
    else:
        return parse_operator(bits[HEAD:], version, type)


def parse_literal(bits, version, type):
    literal_bits = []
    for cur in count(start=0, step=LIT_GROUP):
        literal_bits += bits[cur + 1 : cur + LIT_GROUP]
        if bits[cur] == '0':
            break

    literal = bin_to_dec(''.join(literal_bits))
    packet_len = HEAD + LIT_GROUP + cur

    return Packet(version, type, literal, packet_len)


def parse_operator(bits, version, type):
    if bits[0] == '0':
        bits_len = bin_to_dec(bits[1:OP_BITS])
        return parse_op_with_bits_len(bits[OP_BITS:], bits_len, version, type)
    else:
        num_packets = bin_to_dec(bits[1:OP_PKT])
        return parse_op_with_packet_num(bits[OP_PKT:], num_packets, version, type)


def parse_op_with_bits_len(bits, bits_len, version, type):
    cur = 0
    packets = []
    while cur < bits_len:
        packet = parse_packet(bits[cur:])
        packets.append(packet)
        cur += packet.len

    packet_len = HEAD + OP_BITS + cur

    return Packet(version, type, packets, packet_len)


def parse_op_with_packet_num(bits, num_packets, version, type):
    cur = 0
    packets = []
    for _ in range(num_packets):
        packet = parse_packet(bits[cur:])
        packets.append(packet)
        cur += packet.len

    packet_len = HEAD + OP_PKT + cur

    return Packet(version, type, packets, packet_len)


def version_sum(packet):
    if packet.is_literal():
        return packet.version

    return packet.version + sum(map(version_sum, packet.payload))


def calc_value(packet):
    if packet.is_literal():
        return packet.payload

    operator = operators[packet.type]
    return operator(map(calc_value, packet.payload))


packets = parse_input('input.txt')

assert version_sum(packets) == 1012
assert calc_value(packets) == 2223947372407
