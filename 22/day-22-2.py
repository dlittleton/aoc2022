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


def stitch_faces(faces):
    ''' Arrange faces into a cube '''

    # Faces indexed by grid position
    fgrid = { (f.grid_row, f.grid_col) : f for f in faces }
    print(fgrid)



    # Step one, look for faces directly under or to the right of the current face.
    for f in faces:
        row = f.grid_row
        col = f.grid_col

        right = fgrid.get((row, col + 1), None)
        if right:
            f.link(Direction.Right, right, Direction.Left)

        other = fgrid.get((row + 1, col), None)
        if other:
            f.link(Direction.Down, other, Direction.Up)

    goal_links = 24 # All 6 faces linked on all 4 sides
    link_count = sum(f.link_count for f in faces)
    print('Start link count: ', link_count)    
    while link_count < goal_links:

        faces_with_downlinks = (f for f in faces if Direction.Down in f.links)
        for f in faces_with_downlinks:
            (other, denter, _) = f.links[Direction.Down]

            clockwise = (denter + 1) % len(Direction)
            if clockwise in other.links:
                oclock, enter, _ = other.links[clockwise]
                # Rotate counter clockwise
                enter = (enter + 1) % len(Direction)
                f.link(Direction.Right, oclock, enter)

            # A node to the right of the face below this one is also to the right of this one.
            cclockwise = (denter - 1) % len(Direction)
            if cclockwise in other.links:
                occlock, enter, _ = other.links[cclockwise]
                # Rotate clockwise
                enter = (enter - 1) % len(Direction)
                f.link(Direction.Left, occlock, enter)

        faces_with_rightlinks = (f for f in faces if Direction.Right in f.links)
        for f in faces_with_rightlinks:
            (other, denter, _) = f.links[Direction.Right]

            clockwise = (denter + 1) % len(Direction)
            if clockwise in other.links:
                oclock, enter, _ = other.links[clockwise]
                # Rotate counter clockwise
                enter = (enter + 1) % len(Direction)
                f.link(Direction.Up, oclock, enter)

            # A node to the right of the face below this one is also to the right of this one.
            cclockwise = (denter - 1) % len(Direction)
            if cclockwise in other.links:
                occlock, enter, _ = other.links[cclockwise]
                # Rotate clockwise
                enter = (enter - 1) % len(Direction)
                f.link(Direction.Down, occlock, enter)

        faces_with_leftlinks = (f for f in faces if Direction.Left in f.links)
        for f in faces_with_leftlinks:
            (other, lenter, _) = f.links[Direction.Left]

            clockwise = (lenter + 1) % len(Direction)
            if clockwise in other.links:
                oclock, enter, _ = other.links[clockwise]
                # Rotate counter clockwise
                enter = (enter + 1) % len(Direction)
                f.link(Direction.Down, oclock, enter)

            # A node to the right of the face below this one is also to the right of this one.
            cclockwise = (lenter - 1) % len(Direction)
            if cclockwise in other.links:
                occlock, enter, _ = other.links[cclockwise]
                # Rotate clockwise
                enter = (enter - 1) % len(Direction)
                f.link(Direction.Up, occlock, enter)

        link_count = sum(f.link_count for f in faces)
        print('Current link count: ', link_count)

        
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
        dir_name = Direction(exit_side).name
        if exit_side in self.links:
            return

        print('Node {0} is {1} of node {2}'.format(other_face.name, dir_name, self.name))
        invert = should_invert(exit_side, enter_side)
        self.links[exit_side] = (other_face, enter_side, invert)

        if enter_side not in other_face.links:
            print('Node {0} is {1} of node {2}'.format(self.name, Direction(enter_side).name, other_face.name)) 
            other_face.links[enter_side] = (self, exit_side, invert)

    def __getitem__(self, index):
        x, y = index
        return self.grid[self.row + x, self.col + y]

    @property
    def grid_row(self):
        return self.row // self.size

    @property
    def grid_col(self):
        return self.col // self.size

    @property
    def link_count(self):
        return len(self.links)


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
    f = Face(idx, grid, row, col, face_size)
    faces[f.name] = f

stitch_faces(faces.values())

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