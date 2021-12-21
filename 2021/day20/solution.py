from pathlib import Path
import numpy as np


def parse_input(filename):
    def parse_line(line):
        return [int(char == '#') for char in line]

    algorithm_text, img_text = Path(filename).read_text().split('\n\n')

    algorithm = parse_line(algorithm_text)
    img = np.array([parse_line(line) for line in img_text.splitlines()])

    return algorithm, img


def enhance(img, algorithm):
    enhanced = np.zeros_like(img)

    for coord, _ in np.ndenumerate(enhanced):
        i, j = coord
        sub_mat_3x3 = img[i : i + 3, j : j + 3]
        alg_bin_idx = ''.join(map(str, sub_mat_3x3.flat))
        alg_idx = int(alg_bin_idx, 2)
        enhanced[coord] = algorithm[alg_idx]

    return enhanced


def find_lit_bits(img, algorithm, iterations):
    pad_width = 3 * iterations
    img = np.pad(img, pad_width=pad_width)
    for _ in range(iterations):
        img = enhance(img, algorithm)
    without_pad = img[: (-iterations - 1) * 2, : -iterations * 2]
    return without_pad.sum()


algorithm, img = parse_input('input.txt')

assert find_lit_bits(img, algorithm, 2) == 5680
assert find_lit_bits(img, algorithm, 50) == 19766
