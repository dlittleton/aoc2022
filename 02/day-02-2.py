import sys

values = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 0,
    'Y': 3,
    'Z': 6
}

moves = {}

def add_moves(base, win, lose, draw):
    moves[(base, 'X')] = lose
    moves[(base, 'Y')] = draw
    moves[(base, 'Z')] = win


add_moves('A', 'B', 'C', 'A')
add_moves('B', 'C', 'A', 'B')
add_moves('C', 'A', 'B', 'C')

total = 0
for l in map(str.rstrip, sys.stdin):
    move, goal = l.split()
    play = moves[(move, goal)]
    print(play)
    total += values[play] + values[goal]

print(total)
