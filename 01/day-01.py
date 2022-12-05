import sys


def calculate_groups(lines):
    total = 0
    for line in lines:
        if not line:
            yield total
            total = 0
        else:
            total += int(line)
    yield total


sums = list(calculate_groups(map(str.rstrip, sys.stdin)))
sums.sort(reverse=True)
print(sums[0])
print(sum(s for s in sums[0:3]))
