from pathlib import Path

WIN_LEN = 25


def contains_two_sum(nums, target):
    diffs = set()
    for num in nums:
        if num in diffs:
            return True
        diffs.add(target - num)
    return False


def first_non_valid(nums):
    for i in range(WIN_LEN, len(nums)):
        is_valid = contains_two_sum(nums[i - WIN_LEN: i], nums[i])
        if not is_valid:
            return nums[i]


def contiguous_interval_with_sum(nums, target):
    left = 0
    right = 1
    sum_ = nums[0]

    while sum_ != target:
        if sum_ < target and right < len(nums):
            sum_ += nums[right]
            right += 1
        else:
            sum_ -= nums[left]
            left += 1

    return left, right


nums = [int(line) for line in Path('input.txt').read_text().splitlines()]

first_non_valid_num = first_non_valid(nums)

interval_left, interval_right = contiguous_interval_with_sum(nums, first_non_valid_num)
interval = nums[interval_left: interval_right]


print('part1:', first_non_valid_num)
print('part2:', min(interval) + max(interval))
