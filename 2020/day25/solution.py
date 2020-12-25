from itertools import count


def transform_subject(subj, loop_size):
    value = 1
    for _ in range(loop_size):
        value = value * subj % 20201227
    return value


def get_loop_size(pub_key):
    value = 1
    for loop in count(1):
        value = value * 7 % 20201227
        if value == pub_key:
            return loop


def get_encryption_key(pub_keys):
    loop_size0 = get_loop_size(pub_keys[0])
    return transform_subject(pub_keys[1], loop_size0)


pub_keys = (14012298, 74241)

enc_key = get_encryption_key(pub_keys)

print(enc_key)

assert enc_key == 18608573
