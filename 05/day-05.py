import re
import sys
from collections import deque

move_definition = re.compile(r'move (?P<count>\d+) from (?P<start>\d+) to (?P<end>\d+)')
lines = sys.stdin.readlines()

# 4 characters per stack
crate_size = 4
nstacks = len(lines[0]) // crate_size
stacks = [deque() for n in range(nstacks)]

# Initialize
for last_crate_line, l in enumerate(lines):
    if '[' not in l:
        break

    for i in range(nstacks):
        c = l[i * crate_size + 1]
        if c != ' ':
            stacks[i].appendleft(c)

# Skip numbers and blank line
moves = lines[last_crate_line+2:]

for m in moves:
    match = move_definition.match(m)
    count, start, end = map(int, match.groups())
    for _ in range(count):
        stacks[end-1].append(stacks[start-1].pop())

top_chars = [s.pop() for s in stacks]
print(''.join(top_chars))