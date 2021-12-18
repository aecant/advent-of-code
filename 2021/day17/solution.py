def triangular(x):
    return x * (x + 1) // 2


def hits_target(init_v_x, init_v_y):
    x, y = 0, 0
    v_x, v_y = init_v_x, init_v_y
    while True:
        x += v_x
        y += v_y

        v_x = max(v_x - 1, 0)
        v_y -= 1

        if target_lo_x <= x <= target_hi_x and target_lo_y <= y <= target_hi_y:
            return True

        if y < target_lo_y or x > target_hi_x:
            return False


def solve_part2():
    return sum(
        hits_target(x, y)
        for x in range(target_hi_x + 1)
        for y in range(target_lo_y, 2 - target_lo_y)
    )


target_lo_x, target_hi_x = 150, 193
target_lo_y, target_hi_y = -136, -86

part1 = triangular(-target_lo_y - 1)
part2 = solve_part2()

assert part1 == 9180
assert part2 == 3767
