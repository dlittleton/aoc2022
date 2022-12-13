import re
import sys

from functools import cmp_to_key
from itertools import zip_longest

delims = re.compile(r'([\[\],])')

def pair(it):
    return zip(it, it)

def tokenize(line):
    return (part for part in delims.split(line) if part not in ('', ','))

def parse_list(parts):
    result = []

    for p in parts:
        if p == '[':
            result.append(parse_list(parts))
        elif p == ']':
            return result
        else:
            result.append(int(p))

    return result[0]

def is_list(x):
    return isinstance(x, list)

def ensure_list(x):
    return x if is_list(x) else [x] 

def compare(left, right):
    for l, r in zip_longest(left, right):
        # List exhaustion
        if l is None and r is not None:
            return -1
        elif r is None and l is not None:
            return 1

        if is_list(l) or is_list(r):
            result = compare(ensure_list(l), ensure_list(r))
        else:
            result = l - r

        if result != 0:
            return result

    return 0

        

all_packets = []
results = []
for l, r in pair(filter(lambda x: x, map(str.rstrip, sys.stdin))):
    left = parse_list(tokenize(l))
    right = parse_list(tokenize(r))

    all_packets.append(left)
    all_packets.append(right)

    results.append(compare(left, right) < 0)

total = 0
for i, result in enumerate(results, 1):
    if result:
        total += i

print(total)

div_2 = parse_list(tokenize('[[2]]'))
div_6 = parse_list(tokenize('[[6]]'))

all_packets.append(div_2)
all_packets.append(div_6)

all_packets.sort(key=cmp_to_key(compare))
idx_2 = all_packets.index(div_2) + 1
idx_6 = all_packets.index(div_6) + 1

print(idx_2 * idx_6)