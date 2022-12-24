import sys

from heapq import *

def read_initial(source):
    blizzards = {}

    lines = [l.rstrip() for l in source]
    for row, line in enumerate(lines[1: len(lines) - 1], 1):
        for col, char in enumerate(line[1: len(line) - 1], 1):
            if char != '.':
                blizzards[row, col] = char

    return row, col, blizzards

def children(pos):
    r, c = pos

    yield r, c
    yield r + 1, c
    yield r - 1, c
    yield r, c + 1
    yield r, c - 1
    

class Blizzards:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.hbliz = [set() for _ in range(self.cols)]
        self.vbliz = [set() for _ in range(self.rows)]

    def add(self, pos, char):
        r, c = pos
        if char == '>':
            dr, dc = 0, 1
            target = self.hbliz
        elif char == '<':
            dr, dc = 0, -1
            target = self.hbliz
        elif char == '^':
            dr, dc = -1, 0
            target = self.vbliz
        elif char == 'v':
            dr, dc = 1, 0
            target = self.vbliz
        
        for t in range(len(target)):
            target[t].add((r, c))
            r += dr
            c += dc

            r = 1 + ((r - 1) % self.rows)
            c = 1 + ((c - 1) % self.cols)

    
    def is_clear(self, time, pos):
        hidx = time % self.cols
        vidx = time % self.rows

        return pos not in self.hbliz[hidx] and pos not in self.vbliz[vidx]
        

rows, cols, init = read_initial(sys.stdin)

start = (0, 1)
target = (rows + 1, cols)

blizzards = Blizzards(rows, cols)
for pos, char in init.items():
    blizzards.add(pos, char)

paths = []
heappush(paths, (0, start, 0))

closest = target[0] - start[0] + target[1] - start[1]
seen = set()

while paths:
    _, pos, time = heappop(paths)
    nt = time + 1

    if (pos, time) in seen:
        continue

    seen.add((pos, time))
    
    if pos == target:
        print('Reached exit at time: ', time)
        break

    for cr, cc in children(pos):
        if (1 <= cr <= rows) and (1 <= cc <= cols) or (cr, cc) in (start, target):
            if blizzards.is_clear(nt, (cr, cc)):
                score = target[0] - cr + target[1] - cc
                if score < closest:
                    print('New closest: ', score)
                    closest = score
                paths.append((score + nt, (cr, cc), nt))

