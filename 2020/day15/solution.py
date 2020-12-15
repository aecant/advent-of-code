def nth_num(init_nums, nth):
    last_seen = {val: pos for pos, val in enumerate(init_nums)}

    cur = 0
    for step in range(len(init_nums), nth - 1):
        nxt = step - last_seen.get(cur, step)
        last_seen[cur] = step
        cur = nxt

    return cur


init_nums = [10, 16, 6, 0, 1, 17]


print('part 1:', nth_num(init_nums, 2020))
print('part 2:', nth_num(init_nums, 30000000))
