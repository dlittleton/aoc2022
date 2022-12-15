import re
import sys

position_re = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

# Read target row as parameter since sample and input differ
target_row = int(sys.argv[1])

cols = set()
for line in sys.stdin:
    match = position_re.match(line)
    sx, sy, bx, by = map(int, match.groups())

    d = abs(sx - bx) + abs(sy - by)
    dr = abs(target_row - sy)

    # Distance remaining to use in the x direction
    remaining = d - dr
    if remaining < 0:
        continue

    lo = sx - remaining
    hi = sx + remaining + 1
    for nx in range(lo, hi):
        # Skip if this is the actual position of the beacon
        if target_row == by and nx == bx:
            continue

        cols.add(nx)

print(len(cols))