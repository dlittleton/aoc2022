import re
import sys

position_re = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

# Read target range as parameter
target_range = int(sys.argv[1])


class Sensor:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def perimeter(self):
        x_lo = max(self.x - self.radius - 1, 0)
        x_hi = min(self.x + self.radius + 1, target_range)

        for x in range(x_lo, x_hi + 1):
            yd = self.radius - abs(x - self.x) + 1
            if yd == 0 and 0 <= self.y <= target_range:
                yield (x, self.y)
            else:
                y_hi = self.y + yd
                if y_hi <= target_range:
                    yield(x, self.y + yd)
                
                y_lo = self.y - yd
                if y_lo >= 0:
                    yield(x, self.y - yd)

    def contains(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.radius

sensors = []
for i, line in enumerate(sys.stdin):
    match = position_re.match(line)
    sx, sy, bx, by = map(int, match.groups())

    d = abs(sx - bx) + abs(sy - by)
    sensors.append(Sensor(sx, sy, d))

checked = 0
found = False
for s in sensors:
    for p in s.perimeter():
        if all(not s.contains(*p) for s in sensors):
            found = True
            break

    if found:
        break

print(p[0] * 4000000 + p[1])
        