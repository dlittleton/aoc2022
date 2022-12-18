import sys

from itertools import cycle

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

rock_types = [
    Rock('####'),
    Rock('.#.', '###', '.#.'),
    Rock('..#', '..#', '###'),
    Rock('#', '#', '#', '#'),
    Rock('##', '##')
]
rocks = cycle(rock_types)
wind = cycle(sys.stdin.readline().strip())

rock_count = 2022
tower = [[True] * max_width]
for _ in range(rock_count):
    rock = next(rocks)
    rock.reset(2, len(tower) + 3)

    resting = False
    while not resting:
        print(rock.x, rock.y)
        w = next(wind)
        if w == '<':
            rock.move_left(tower)
        elif w == '>':
            rock.move_right(tower)
        else:
            raise ValueError('Unexpected wind value! \"{0}\"'.format(w))
        
        resting = rock.drop(tower)

    print(rock.x, rock.y)
    for x, y in rock.points():
        while y >= len(tower):
            tower.append([False] * max_width)
        tower[y][x] = True

print(len(tower) - 1)


