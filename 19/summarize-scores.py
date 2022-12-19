import sys

# Post process part one output to calculate quality level
temp = [int(l.rstrip()) for l in sys.stdin.readlines()[1::2]]
print(sum(i * t for i, t in enumerate(temp, 1)))