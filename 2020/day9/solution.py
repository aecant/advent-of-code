from pathlib import Path

WIN_LEN = 25


def contains_two_sum(nums, target):
    diffs = set()
    for num in nums:
        if num in diffs:
            return True
        diffs.add(target - num)
    return False


def is_valid(nums, idx):
    return contains_two_sum(nums[idx - WIN_LEN: idx], nums[idx])


def first_non_valid(nums):
    return next(nums[i] for i in range(WIN_LEN, len(nums)) if not is_valid(nums, i))


def contiguous_interval_with_sum(nums, target):
    left, right = 0, 1
    sum_ = nums[0]

    while sum_ != target:
        if sum_ < target:
            sum_ += nums[right]
            right += 1
        else:
            sum_ -= nums[left]
            left += 1

    return left, right


def solve_part2(nums, first_non_valid_num):
    interval_left, interval_right = contiguous_interval_with_sum(nums, result_part1)
    interval = nums[interval_left: interval_right]
    return min(interval) + max(interval)


nums = [int(line) for line in Path('input.txt').read_text().splitlines()]

result_part1 = first_non_valid(nums)
result_part2 = solve_part2(nums, result_part1)

print('part1:', result_part1)
print('part2:', result_part2)

assert result_part1 == 731031916
assert result_part2 == 93396727
