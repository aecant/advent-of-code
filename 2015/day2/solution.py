from pathlib import Path


def parse_dim(line):
    return sorted(map(int, line.split('x')))


def paper_surface(w, l, h):
    area = 2 * l * w + 2 * w * h + 2 * h * l
    slack = w * l
    return area + slack


def ribbon_len(w, l, h):
    wrap = 2 * w + 2 * l
    bow = w * l * h
    return wrap + bow


lines = Path('input.txt').read_text().splitlines()
dimensions = list(map(parse_dim, lines))

print(sum(paper_surface(w, l, h) for w, l, h in dimensions))
print(sum(ribbon_len(w, l, h) for w, l, h in dimensions))
