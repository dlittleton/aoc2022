import re
import sys

from collections import defaultdict, namedtuple
from enum import IntEnum
from itertools import zip_longest

class Direction(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

def should_invert(exit, enter):
    ''' True if index should be inverted based on a particular side pairing'''
    lo, hi = sorted((exit, enter))
    
    if lo == Direction.Right and (hi == Direction.Left or hi == Direction.Down):
        return False
    
    if lo == Direction.Down and hi == Direction.Up:
        return False

    if lo == Direction.Left and hi == Direction.Up:
        return False

    return True

def dir_to_offsets(idx):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return directions[idx % len(directions)]

def read_grid(spec):
    ''' Read map information'''
    grid = defaultdict(lambda: ' ')
    for row, line in enumerate(spec, 1):
        if not line:
            break
        
        for col, char in enumerate(line, 1):
            grid[row, col] = char

    return grid 


def find_faces(grid, face_size):
    ''' Look for cube start positions. '''
    face_idx = 0
    for x in range(4):
        for y in range(4):
            r = x * face_size + 1
            c = y * face_size + 1
            if grid[r, c] != ' ':
                face_idx += 1
                yield face_idx, r, c


def get_enter_position(enter_side, idx):
    positions = {
        Direction.Right: (idx, face_size - 1),
        Direction.Down: (face_size - 1, idx),
        Direction.Left: (idx, 0),
        Direction.Up: (0, idx)
    }

    return positions[enter_side]


class Face:
    ''' Individual face with local coordinates '''

    def __init__(self, name, grid, row, col, size):
        self.name = name
        self.grid = grid
        self.row = row
        self.col = col
        self.size = size
        self.links = {}

    def link(self, exit_side, other_face, enter_side):
        invert = should_invert(exit_side, enter_side)
        self.links[exit_side] = (other_face, enter_side, invert) 

    def check_links(self):
        for link in self.links:
            cube, enter_side, invert = self.links[link]

            oface, oenter, oinvert = cube.links[enter_side]

            matches = oface.name == self.name and oenter == link and oinvert == invert
            if not matches:
                print("Checking face {0} link {1}".format(self.name, link))
                print(self.name, oface.name)
                print(link, oenter)
                print(invert, oinvert)
                print("")

    def __getitem__(self, index):
        x, y = index
        return self.grid[self.row + x, self.col + y]


class Cursor(namedtuple('Cursor', ['face', 'x', 'y', 'direction'])):
    ''' Current position '''
    
    def rotate(self, k):
        if k == 'R':
            return Cursor(self.face, self.x, self.y, (self.direction + 1) % len(Direction))
        elif k == 'L':
            return Cursor(self.face, self.x, self.y, (self.direction - 1) % len(Direction))
        else:
            return self

    def advance(self):
        ''' Advance cursor one position, switching faces if necessary '''
        dx, dy = dir_to_offsets(self.direction)

        nx, ny = self.x + dx, self.y + dy

        xvalid = 0 <= nx < face_size
        yvalid = 0 <= ny < face_size

        if xvalid and yvalid:
            return Cursor(self.face, nx, ny, self.direction)

        valid_index = self.y if yvalid else self.x
        face, enter_side, invert = self.face.links[self.direction]
        if invert:
            valid_index = (face_size - 1) - valid_index
            
        nx, ny = get_enter_position(enter_side, valid_index)
        new_dir = (enter_side + 2) % len(Direction) # Direction is opposite of entry side

        return Cursor(face, nx, ny, new_dir)

    @property
    def value(self):
        return self.face[self.x, self.y]

    @property
    def grid_position(self):
        return self.x + self.face.row, self.y + self.face.col



face_size = int(sys.argv[1])
input = map(str.rstrip, sys.stdin)

grid = read_grid(input)
moves = re.split(r'(L|R)', next(input))

faces = {}
for idx, row, col in find_faces(grid, face_size):
    faces[idx] = Face(idx, grid, row, col, face_size)

if face_size == 4:
    # Setup Links For Sample
    faces[1].link(Direction.Right, faces[6], Direction.Right)
    faces[1].link(Direction.Down, faces[4], Direction.Up)
    faces[1].link(Direction.Left, faces[3], Direction.Up)
    faces[1].link(Direction.Up, faces[2], Direction.Up)

    faces[2].link(Direction.Right, faces[3], Direction.Left)
    faces[2].link(Direction.Down, faces[5], Direction.Down)
    faces[2].link(Direction.Left, faces[6], Direction.Down)
    faces[2].link(Direction.Up, faces[1], Direction.Up)

    faces[3].link(Direction.Right, faces[4], Direction.Left)
    faces[3].link(Direction.Down, faces[5], Direction.Left)
    faces[3].link(Direction.Left, faces[2], Direction.Right)
    faces[3].link(Direction.Up, faces[1], Direction.Left)

    faces[4].link(Direction.Right, faces[6], Direction.Up)
    faces[4].link(Direction.Down, faces[5], Direction.Up)
    faces[4].link(Direction.Left, faces[3], Direction.Right)
    faces[4].link(Direction.Up, faces[1], Direction.Down)

    faces[5].link(Direction.Right, faces[6], Direction.Left)
    faces[5].link(Direction.Down, faces[2], Direction.Down)
    faces[5].link(Direction.Left, faces[3], Direction.Down)
    faces[5].link(Direction.Up, faces[4], Direction.Down)

    faces[6].link(Direction.Right, faces[1], Direction.Right)
    faces[6].link(Direction.Down, faces[2], Direction.Left)
    faces[6].link(Direction.Left, faces[5], Direction.Right)
    faces[6].link(Direction.Up, faces[4], Direction.Right)
else:
    # Setup links for input
    faces[1].link(Direction.Right, faces[2], Direction.Left)
    faces[1].link(Direction.Down, faces[3], Direction.Up)
    faces[1].link(Direction.Left, faces[4], Direction.Left)
    faces[1].link(Direction.Up, faces[6], Direction.Left)

    faces[2].link(Direction.Right, faces[5], Direction.Right)
    faces[2].link(Direction.Down, faces[3], Direction.Right)
    faces[2].link(Direction.Left, faces[1], Direction.Right)
    faces[2].link(Direction.Up, faces[6], Direction.Down)

    faces[3].link(Direction.Right, faces[2], Direction.Down)
    faces[3].link(Direction.Down, faces[5], Direction.Up)
    faces[3].link(Direction.Left, faces[4], Direction.Up)
    faces[3].link(Direction.Up, faces[1], Direction.Down)

    faces[4].link(Direction.Right, faces[5], Direction.Left)
    faces[4].link(Direction.Down, faces[6], Direction.Up)
    faces[4].link(Direction.Left, faces[1], Direction.Left)
    faces[4].link(Direction.Up, faces[3], Direction.Left)

    faces[5].link(Direction.Right, faces[2], Direction.Right)
    faces[5].link(Direction.Down, faces[6], Direction.Right)
    faces[5].link(Direction.Left, faces[4], Direction.Right)
    faces[5].link(Direction.Up, faces[3], Direction.Down)

    faces[6].link(Direction.Right, faces[5], Direction.Down)
    faces[6].link(Direction.Down, faces[2], Direction.Up)
    faces[6].link(Direction.Left, faces[1], Direction.Up)
    faces[6].link(Direction.Up, faces[4], Direction.Down)

for f in faces.values():
    f.check_links()

cursor = Cursor(faces[1], 0, 0, Direction.Right)
move_iterator = iter(moves)
for n, turn in zip_longest(move_iterator, move_iterator):
    n = int(n)
    for _ in range(n):
        ncursor = cursor.advance()
        if ncursor.value == '#':
            break
        cursor = ncursor

    cursor = cursor.rotate(turn)

r, c = cursor.grid_position
v = (r * 1000) + (c * 4) + cursor.direction
print(v)