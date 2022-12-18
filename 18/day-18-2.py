import sys

from collections import deque
from enum import Enum

State = Enum('State', ['air', 'steam', 'lava'])

def neighbors(x, y, z):
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1

def get_range(positions, idx):
    values = [p[idx] for p in positions]
    return min(values) - 1, max(values) + 1

def parse(line):
    return tuple(map(int, line.rstrip().split(',')))

positions = [parse(l) for l in sys.stdin]
xvals = get_range(positions, 0)
yvals = get_range(positions, 1)
zvals = get_range(positions, 2)

points = {}
# Set lava
for p in positions:
    points[p] = State.lava

# Fill with air
for x in range(xvals[0], xvals[1] + 1):
    for y in range(yvals[0], yvals[1] + 1):
        for z in range(zvals[0], zvals[1] + 1):
            if (x, y, z) not in points:
                points[(x,y,z)] = State.air

# Assign steam to lowest coordinate
lo = (xvals[0], yvals[0], zvals[0])
points[lo] = State.steam

# Flood fill
heads = deque()
heads.append(lo)
while heads:
    h = heads.popleft()
    for n in neighbors(*h):
        if points.get(n, State.steam) == State.air:
            points[n] = State.steam
            heads.append(n)

# Count sides exposed to steam
total = 0
for p in positions:
    for n in neighbors(*p):
        if points[n] == State.steam:
            total += 1

print(total)