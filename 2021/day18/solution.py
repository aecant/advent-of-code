from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import reduce
from itertools import permutations
from pathlib import Path


@dataclass
class Node:
    val: int | tuple[Node, Node]

    def __add__(self, o):
        res = Node((self, o)).copy()
        while res.explode() or res.split():
            pass
        return res

    def copy(self):
        if self.is_leaf():
            return Node(self.val)
        return Node((self.val[0].copy(), self.val[1].copy()))

    def is_leaf(self):
        return isinstance(self.val, int)

    def explode(self):
        last_visited = None
        exploded_right = None
        to_visit = [(self, 0)]

        while to_visit:
            node, depth = to_visit.pop()
            if node.is_leaf():
                if exploded_right:
                    node.val += exploded_right.val
                    return True
                last_visited = node
            elif depth == 4 and not exploded_right:
                if last_visited:
                    last_visited.val += node.val[0].val
                exploded_right = node.val[1]
                node.val = 0
            else:
                to_visit.append((node.val[1], depth + 1))
                to_visit.append((node.val[0], depth + 1))

        return False

    def split(self):
        if self.is_leaf():
            if self.val < 10:
                return False
            left_val = math.floor(self.val / 2)
            right_val = math.ceil(self.val / 2)
            self.val = Node(left_val), Node(right_val)
            return True

        return self.val[0].split() or self.val[1].split()

    def magnitude(self):
        if self.is_leaf():
            return self.val

        return 3 * self.val[0].magnitude() + 2 * self.val[1].magnitude()

    @staticmethod
    def from_list(lst: list) -> Node:
        if isinstance(lst, int):
            return Node(lst)
        return Node((Node.from_list(lst[0]), Node.from_list(lst[1])))


def parse_nodes(filename):
    return [
        Node.from_list(json.loads(line)) for line in Path(filename).read_text().splitlines()
    ]


nodes = parse_nodes('input.txt')

part1 = reduce(Node.__add__, nodes).magnitude()
part2 = max((n1 + n2).magnitude() for n1, n2 in permutations(nodes, 2))

assert part1 == 4433
assert part2 == 4559
