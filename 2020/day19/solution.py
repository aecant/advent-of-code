import re
from functools import cache
from pathlib import Path


def parse_rule(rule_line):
    idx, rule_str = rule_line.split(':')
    idx = int(idx)

    if match_terminal_rule := re.match(r'"(\w)"', rule_str.strip()):
        sub_rule = match_terminal_rule.group(1)
    else:
        sub_rule_ids = re.findall(r'(\d+)( \d+)*', rule_str)
        sub_rule = [
            tuple(int(id_) for id_ in sub_rule_id if id_)
            for sub_rule_id in sub_rule_ids
        ]

    return idx, sub_rule


def create_regex(rules):
    @cache
    def create_regex_rec(rule_id):
        if isinstance(rules[rule_id], str):
            return rules[rule_id]

        rules_str = '|'.join(
            ''.join(create_regex_rec(sub_rule_id) for sub_rule_id in or_expr_list)
            for or_expr_list in rules[rule_id]
        )
        return f'({rules_str})'

    return create_regex_rec(0)


def count_correct_messages(rules, messages):
    pattern = create_regex(rules)
    pattern = f'^{pattern}$'
    return sum(bool(re.match(pattern, msg)) for msg in messages)


def get_new_rules(rules):
    repetitions = range(1, 6)  # arbitrarily choosen big enough
    return {
        **rules,
        8: [(42,) * n for n in repetitions],
        11: [(42,) * n + (31,) * n for n in repetitions],
    }


rules_txt, messages_txt = Path('input.txt').read_text().split('\n\n')

rules = dict(map(parse_rule, rules_txt.splitlines()))
new_rules = get_new_rules(rules)
messages = messages_txt.splitlines()

result_part1 = count_correct_messages(rules, messages)
result_part2 = count_correct_messages(new_rules, messages)


assert result_part1 == 241
assert result_part2 == 424
