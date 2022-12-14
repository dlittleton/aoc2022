import sys

from collections import defaultdict
from itertools import chain

def sign(x):
    return 0 if x == 0 else x // abs(x)

def tokenize(line):
    points = line.split('->')
    coordinates = (p.split(',') for p in points)
    points = map(int, map(str.rstrip, chain(*coordinates)))
    return list(zip(points, points))

def get_rocks(points):
    prev = points[0]
    yield prev

    for next in points[1:]:
        diff = (sign(next[0] - prev[0]), sign(next[1] - prev[1]))

        while prev != next:
            prev = (prev[0] + diff[0], prev[1] + diff[1])
            yield prev

def down(p):
    x, y = p
    return (x, y + 1)

def left(p):
    x, y = p
    return (x - 1, y + 1)

def right(p):
    x, y = p
    return (x + 1, y + 1)

def move_sand(s, grid):
    moves = [down(s), left(s), right(s)]
    for m in moves:
        if grid[m] == '.':
            return m

    return s



def drop_sand(grid, low):
    while True:
        cur = (500, 0)
        next = move_sand(cur, grid)
        while next != cur:
            cur = next
            next = move_sand(cur, grid)
            if next[1] > low:
                return

        grid[next] = 'O'


grid = defaultdict(lambda: '.')
lowest_point = 0
for l in sys.stdin:
    p = tokenize(l)
    
    for r in get_rocks(p):
        grid[r] = '#'
        lowest_point = max(lowest_point, r[1])

drop_sand(grid, lowest_point)
total = sum(1 for v in grid.values() if v == 'O')
print(total)