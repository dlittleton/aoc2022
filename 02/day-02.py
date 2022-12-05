import sys

scorecard = {}


def make_scorecard(symbol, value, win, lose, draw):
    scorecard[(win, symbol)] = value + 6
    scorecard[(draw, symbol)] = value + 3
    scorecard[(lose, symbol)] = value


make_scorecard('X', 1, 'C', 'B', 'A')
make_scorecard('Y', 2, 'A', 'C', 'B')
make_scorecard('Z', 3, 'B', 'A', 'C')

score = 0
for l in map(str.rstrip, sys.stdin):
    a, b = l.split()
    score += scorecard[(a, b)]

print(score)
