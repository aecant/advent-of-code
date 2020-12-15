import hashlib
import itertools


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def md5_starts_with(s, prefix):
    return next(num for num in itertools.count() if md5(f'{s}{num}').startswith(prefix))


inp = 'iwrupvqb'

print(md5_starts_with(inp, '00000'))
print(md5_starts_with(inp, '000000'))
