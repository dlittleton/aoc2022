import sys

def range_to_set(spec):
    lo, hi = map(int, spec.split('-'))
    return set(range(lo, hi + 1))

count = 0
for line in map(str.rstrip, sys.stdin):
    a, b = map(range_to_set, line.split(','))
    if a.issubset(b) or b.issubset(a):
        count += 1

print(count)