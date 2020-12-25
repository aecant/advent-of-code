import operator
from pathlib import Path


def second_arg(_, y):
    return y


def resolve_expr_wo_prec(tokens):
    op = second_arg
    value = None
    while tokens:
        token = tokens.pop()

        if token == ')':
            return value

        if token == '(':
            value = op(value, resolve_expr_wo_prec(tokens))
        elif token.isdigit():
            value = op(value, int(token))
        elif token == '+':
            op = operator.add
        else:
            op = operator.mul

    return value


def resolve_expr_with_prec(tokens):
    op = second_arg
    value = None
    while tokens:
        token = tokens.pop()

        if token == ')':
            return value
        if token == '*':
            return value * resolve_expr_with_prec(tokens)

        if token == '(':
            value = op(value, resolve_expr_with_prec(tokens))
        elif token.isdigit():
            value = op(value, int(token))
        else:
            op = operator.add

    return value


def parse_tokens(line):
    return list(reversed(line.replace(' ', '')))


lines = Path('input.txt').read_text().splitlines()

result_part1 = sum(map(resolve_expr_wo_prec, map(parse_tokens, lines)))
result_part2 = sum(map(resolve_expr_with_prec, map(parse_tokens, lines)))

print(result_part1)
print(result_part2)

assert result_part1 == 464478013511
assert result_part2 == 85660197232452
