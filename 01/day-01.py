import sys

def calculateGroups(lines):
    total = 0
    for line in lines:
        if not line:
            yield total
            total = 0
        else:
            total += int(line)


sums = calculateGroups(map(str.rstrip, sys.stdin))
print(max(sums))