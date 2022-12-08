import sys

heights = {}

for row, line in enumerate(map(str.rstrip, sys.stdin)):
    for col, h in enumerate(line):
        heights[(row, col)] = int(h)

nrows = row + 1
ncols = col + 1

visibility = {}


# Left to right
for r in range(nrows):
    last_height = -1
    for c in range(ncols):
        if heights[(r,c)] > last_height:
            last_height = heights[(r,c)]
            visibility[(r,c)] = True

# Right to left
for r in range(nrows):
    last_height = -1
    for c in reversed(range(ncols)):
        if heights[(r,c)] > last_height:
            last_height = heights[(r,c)]
            visibility[(r,c)] = True

# Top down
for c in range(ncols):
    last_height = -1
    for r in range(nrows):
        if heights[(r,c)] > last_height:
            last_height = heights[(r,c)]
            visibility[(r,c)] = True

# Bottom up
for c in range(ncols):
    last_height = -1
    for r in reversed(range(nrows)):
        if heights[(r,c)] > last_height:
            last_height = heights[(r,c)]
            visibility[(r,c)] = True

print(len(visibility))