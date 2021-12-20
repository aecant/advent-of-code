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
    enhanced = np.pad(np.zeros_like(img), pad_width=1)
    padded_img = np.pad(img, pad_width=2)

    for coord, _ in np.ndenumerate(enhanced):
        i, j = coord
        sub_mat_3x3 = padded_img[i : i + 3, j : j + 3]
        alg_bin_idx = ''.join(map(str, sub_mat_3x3.flat))
        alg_idx = int(alg_bin_idx, 2)
        pixel = algorithm[alg_idx]
        enhanced[coord] = pixel

    return enhanced


def to_str(img):
    def row_to_str(row):
        return ''.join('#' if val else '.' for val in row)

    return '\n'.join(map(row_to_str, img))


# NOT 5708,5565
algorithm, img = parse_input('test_input.txt')
# algorithm, img = parse_input('input.txt')


# print(img.shape)
enhanced = enhance(img, algorithm)
enhanced2 = enhance(enhanced, algorithm)
# print(to_str(enhanced2))
print(enhanced2.sum())
