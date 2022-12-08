import sys

heights = {}

for row, line in enumerate(map(str.rstrip, sys.stdin)):
    for col, h in enumerate(line):
        heights[(row, col)] = int(h)

nrows = row + 1
ncols = col + 1

scenic = {}

def countdown(x):
    ''' Range descending to 0 '''
    return range(x-1, -1, -1)

def calculate_score(tr, tc):
    target = heights[(tr, tc)]
    
    # Look left    
    left = 0
    for c in countdown(tc):
        left += 1
        if heights[(tr, c)] >= target:
            break

    # Look up
    up = 0
    for r in countdown(tr):
        up += 1
        if heights[(r, tc)] >= target:
            break


    # Look right
    right = 0
    for c in range(tc + 1, ncols):
        right += 1
        if heights[(tr, c)] >= target:
            break

    # Look down
    down = 0
    for r in range(tr + 1, nrows):
        down += 1
        if heights[(r, tc)] >= target:
            break

    return left * up * right * down


for tr in range(nrows):
    for tc in range(ncols):
        scenic[(tr, tc)] = calculate_score(tr, tc)

print(max(scenic.values()))