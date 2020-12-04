from pathlib import Path
import math

def count_trees(lines, right, down):
    count = 0
    i, j = down, right
    while i < len(lines):
        if lines[i][j] == '#':
            count += 1
        i += down
        j += right
        if j >= len(lines[0]):
            j -= len(lines[0])

    return count


lines = Path('input.txt').read_text().splitlines()

part1_result = count_trees(lines, 3, 1)

part2_directions = [(1,1), (3,1), (5,1), (7,1), (1,2)]
part2_result = math.prod(count_trees(lines, right, down) for right, down in part2_directions)

print('part1:', part1_result)
print('part2:', part2_result)
