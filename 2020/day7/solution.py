import re
from pathlib import Path
from collections import defaultdict


def parse_rule(s):
    parent = ' '.join(s.split()[:2])
    children = [(int(qty), child) for qty, child in re.findall(r'(\d+) (\w+ \w+) bags?[,.]', s)]
    return parent, children


def reverse_graph(children):
    dic = defaultdict(list)
    for parent, children in children.items():
        for _, child in children:
            dic[child].append(parent)

    return dic


def count_possible_parents(bag, parents_dict):
    queue = parents_dict[bag].copy()
    counted = set()
    while queue:
        bag = queue.pop()
        if bag not in counted:
            queue.extend(parents_dict[bag])
            counted.add(bag)

    return len(counted)


def count_required_children(bag, children, cache={}):
    if not children[bag]:
        return 1
    if bag not in cache:
        cache[bag] = 1 + sum(count_required_children(child, children, cache) * qty for qty, child in children[bag])

    return cache[bag]


lines = Path('input.txt').read_text().splitlines()

children = dict(map(parse_rule, lines))
parents = reverse_graph(children)

result_part1 = count_possible_parents('shiny gold', parents)
result_part2 = count_required_children('shiny gold', children) - 1

print('part1:', result_part1)
print('part2:', result_part2)

result_part1 = 278
result_part2 = 45157
