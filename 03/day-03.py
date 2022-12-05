import sys

def get_priority(x):
    if 'a' <= x <= 'z':
        return (ord(x) - ord('a')) + 1
    else:
        return (ord(x) - ord('A')) + 27


def find_duplicate(x):
    half = len(x) // 2
    first = set(x[:half])
    second = set(x[half:])
    return first.intersection(second).pop()

total = 0
for l in map(str.rstrip, sys.stdin):
    dup = find_duplicate(l)
    total += get_priority(dup)

print(total)