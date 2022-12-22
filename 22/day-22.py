import re
import sys

from collections import defaultdict
from enum import Enum
from itertools import zip_longest

Terrain = Enum('Terain', ['void', 'open', 'wall'])

def move(pos, dir):
    x, y = pos[0] + dir[0], pos[1] + dir[1]
    if grid[x, y] != Terrain.void:
        return x, y

    if dir == (0, 1):
        y = rows[x][0]
    elif dir == (1, 0):
        x = cols[y][0]
    elif dir == (0, -1):
        y = rows[x][1]
    elif dir == (-1, 0):
        x = cols[y][1]
    else:
        raise ValueError('Invalid direction')

    return x, y

char_to_terrain = {
    ' ': Terrain.void,
    '.': Terrain.open,
    '#': Terrain.wall
}

input = map(str.rstrip, sys.stdin)

grid = defaultdict(lambda: Terrain.void)
rows = {}
cols = {}

for row, line in enumerate(input, 1):
    if not line:
        break

    parsed = [(col, char_to_terrain[char]) for col, char in enumerate(line, 1) if char != ' ']
    
    lo = min(c for c, _ in parsed)
    hi = max(c for c, _ in parsed)
    rows[row] = (lo, hi)

    for col, t in parsed:
        grid[(row, col)] = t

        clo, chi = cols.get(col, (row, row))
        cols[col] = (clo, row)

moves = iter(re.split(r'(L|R)', next(input)))

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

pos = (1, rows[1][0])
dir_idx = 0
dir = directions[dir_idx]

for count, turn in zip_longest(moves, moves):
    count = int(count)
    
    for _ in range(count):
        npos = move(pos, dir)

        t = grid[npos]
        if t == Terrain.wall:
            break
        pos = npos

    if turn == 'L':
        dir_idx -= 1
    elif turn == 'R':
        dir_idx += 1
    else:
        print('Unknown direction', turn)

    dir = directions[dir_idx % len(directions)]

x, y = pos
facing = dir_idx % len(directions)

print(x, y, facing)
total = (1000 * x) + (4 * y) + facing
print(total)
