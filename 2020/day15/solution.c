#include <stdio.h>
#include <stdlib.h>

#define NOT_SEEN -1

int nth_num(int init_nums[], int init_nums_len, int nth) {
    int *last_seen = malloc(nth * sizeof(int));
    for (int i = nth - 1; i >= 0; --i) {
        last_seen[i] = NOT_SEEN;
    }

    for (int i = 0; i < init_nums_len; ++i) {
        last_seen[init_nums[i]] = i;
    }

    int curr = 0;
    int next;
    for (int step = init_nums_len; step < nth - 1; ++step) {
        if (last_seen[curr] == NOT_SEEN) {
            next = 0;
        } else {
            next = step - last_seen[curr];
        }
        last_seen[curr] = step;
        curr = next;
    }

    free(last_seen);

    return curr;
}

int main() {
    int init_nums[] = {10, 16, 6, 0, 1, 17};
    int init_nums_len = sizeof(init_nums) / sizeof(init_nums[0]);

    printf("part1: %d\n", nth_num(init_nums, init_nums_len, 2020));
    printf("part2: %d\n", nth_num(init_nums, init_nums_len, 30000000));
}
