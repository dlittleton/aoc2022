import sys
from collections import deque


def get_height(c):
    return ord(c) - ord('a')

paths = []
elevations = []
targets = []

for x, l in enumerate(map(str.rstrip, sys.stdin)):
    row = []
    for y, c in enumerate(l):
        if c == 'S':
            c = 'a'
        elif c == 'E':
            start = (x, y)
            c = 'z'

        if c == 'a':
            targets.append((x, y))
        
        height = get_height(c)
        row.append(height)
    
    p = [-1 for _ in row]
    elevations.append(row)
    paths.append(p)

max_x, max_y = x, y

heads = deque()
heads.append((*start, 0))

while heads:
    x, y, depth = heads.popleft()
    
    if paths[x][y] > -1:
        continue

    paths[x][y] = depth
    current_elevation = elevations[x][y]

    successors = []
    if x > 0:
        successors.append((x - 1, y))
    if x < max_x:
        successors.append((x + 1, y))
    if y > 0:
        successors.append((x, y - 1))
    if y < max_y:
        successors.append((x, y + 1))

    for sx, sy in successors:
        new_elevation = elevations[sx][sy]
        if current_elevation - new_elevation <= 1:
            heads.append((sx, sy, depth + 1))

shortest = min(paths[x][y] for x, y in targets if paths[x][y] != -1)
print(shortest)