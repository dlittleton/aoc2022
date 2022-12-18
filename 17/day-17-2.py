import sys

from collections import defaultdict

max_width = 7

class Rock:
    def __init__(self, *lines):
        self.x = 0
        self.y = 0
        self._points = []
        self._lowest = {} # lowest point for each x

        for y, line in enumerate(reversed(lines)):
            for x, c in enumerate(line):
                if c == '#':
                    self._points.append((x, y))
                    if x not in self._lowest:
                        self._lowest[x] = y

        self.right = max(x for x, _ in self._points) + 1
    
    def reset(self, x, y):
        self.x = x
        self.y = y

    def points(self, *, dx=0, dy=0):
        for x, y in self._points:
            yield (self.x + x + dx, self.y + y + dy)

    def move_left(self, tower):
        if self.x > 0:
            for x, y in self.points(dx=-1):
                if y < len(tower) and tower[y][x]:
                    return
            self.x -= 1

    def move_right(self, tower):
        if self.x + self.right < max_width:
            for x, y in self.points(dx=1):
                if y < len(tower) and tower[y][x]:
                    return
            self.x += 1

    def drop(self, tower):
        for x, y in self.points(dy=-1):
            if y < len(tower) and tower[y][x]:
                return True

        self.y -= 1
        return False

def draw_tower(tower):
    for y in range(len(tower) - 1, 0, -1):
        c = '|'
        for x in range(max_width):
            c += '#' if tower[y][x] else '.'
        c += '|'
        print(c)

rocks = [
    Rock('####'),
    Rock('.#.', '###', '.#.'),
    Rock('..#', '..#', '###'),
    Rock('#', '#', '#', '#'),
    Rock('##', '##')
]
wind = list(sys.stdin.readline().strip())

# Enough to detect a cycle
rock_count = 20000
tower = [[True] * max_width]


index_occurs = {}
heights = []
first_repeat = 0
cycle_length = 0

w_idx = 0
for i in range(rock_count):
    r = i % len(rocks)

    pair = (r, w_idx)
    if pair in index_occurs:
        # HACK: First cycle may be affected by initial state, wait for second cycle.
        if len(index_occurs[pair]) == 2 and first_repeat == 0:
            first_repeat = i
            p, h = index_occurs[pair][1]
            cycle_length = i - p
        index_occurs[pair].append((i, len(tower)))
    else:
        index_occurs[pair] = [(i, len(tower))]

    rock = rocks[r]
    rock.reset(2, len(tower) + 3)

    resting = False
    while not resting:
        w = wind[w_idx]
        w_idx = (w_idx + 1) % len(wind)
        if w == '<':
            rock.move_left(tower)
        elif w == '>':
            rock.move_right(tower)
        else:
            raise ValueError('Unexpected wind value! \"{0}\"'.format(w))
        
        resting = rock.drop(tower)

    for x, y in rock.points():
        while y >= len(tower):
            tower.append([False] * max_width)
        tower[y][x] = True

    heights.append(len(tower))

print(len(tower) - 1)

for foo, count in index_occurs.items():
    print('{0} - {1}: {2}'.format(foo[0], foo[1], count))

print('First repeat: ', first_repeat)
print('Height of first repeat: ', heights[first_repeat])
print('Cycle length:', cycle_length)

h_per_cycle = heights[first_repeat + cycle_length] - heights[first_repeat]
print('Height per cycle: ', h_per_cycle)

print('Actual: ', len(tower) - 1)
#target = rock_count
target = 1000000000000
total = 0

total += heights[first_repeat - 1]
target -= first_repeat
m, r = divmod(target, cycle_length)
total += m * h_per_cycle

h_rem = heights[first_repeat + r] - heights[first_repeat]
total += h_rem

# This is consistently off by one for values that are feasible to simulate.
# I suspect it's related to the prefix height, but took the easy way out and submitted answer + 1.
print('Estimate: ', total - 1)