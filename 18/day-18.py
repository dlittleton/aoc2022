import sys

def neighbors(x, y, z):
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1

def parse(line):
    return tuple(map(int, line.rstrip().split(',')))

points = set(map(parse, sys.stdin))

exposed = 0
for p in points:
    for n in neighbors(*p):
        if n not in points:
            exposed += 1

print(exposed)