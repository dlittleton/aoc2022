import sys

from collections import namedtuple, defaultdict
from enum import IntEnum

class Direction(IntEnum):
    ''' Availalble directions based on order'''
    North = 0
    South = 1
    West = 2
    East = 3

MoveOption = namedtuple('MoveOption', ['offset', 'to_check'])

dir_to_options = {
    Direction.North: MoveOption((-1, 0), [(-1, -1), (-1, 0), (-1, 1)]),
    Direction.East: MoveOption((0, 1), [(-1, 1), (0, 1), (1, 1)]),
    Direction.South: MoveOption((1, 0), [(1, -1), (1, 0), (1, 1)]),
    Direction.West: MoveOption((0, -1), [(-1, -1), (0, -1), (1, -1)])
}

def get_options(start):
    for i in range(len(Direction)):
        yield dir_to_options[(start + i) % len(Direction)]


all_neighbors = set()
for option in get_options(Direction.North):
    for p in option.to_check:
        all_neighbors.add(p)


grid = {}
lines = enumerate(map(str.rstrip, sys.stdin))
for r, line in lines:
    for c, char in enumerate(line):
        if char == '#':
            grid[r, c] = True

starting_dir = Direction.North
rounds = 10

for round in range(rounds):
    proposed_moves = defaultdict(lambda: [])

    print('Starting dir is ', Direction(starting_dir).name)

    # Step 1: Propose moves
    for elf_x, elf_y in grid:
        # First check if we have any neighbors.
        to_check = [(x + elf_x, y + elf_y) for x, y in all_neighbors]
        if all(p not in grid for p in to_check):
            continue

        # Next check directions in order.
        for option in get_options(starting_dir):
            to_check = [(x + elf_x, y + elf_y) for x, y in option.to_check]

            if all(p not in grid for p in to_check):
                target = elf_x + option.offset[0], elf_y + option.offset[1]
                proposed_moves[target].append((elf_x, elf_y))
                break

    # Step 2: Perform moves
    for target, source in proposed_moves.items():
        # Skip duplicate moves
        if len(source) > 1:
            continue

        grid[target] = True
        del grid[source[0]]

    print(len(grid))


    print('End of round {0}'.format(round + 1))
    
    # Shift starting direction
    starting_dir = (starting_dir + 1)% len(Direction)



min_x = min(x for x, _ in grid)
max_x = max(x for x, _ in grid)
min_y = min(y for _, y in grid)
max_y = max(y for _, y in grid)

dx = max_x - min_x + 1
dy = max_y - min_y + 1

area = dx * dy
open = area - len(grid)
print(open)