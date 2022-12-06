import sys

def group(n, spec):
    nspec = len(spec)
    for i in range(nspec):
        yield i, spec[i:i+n]

size = 4
spec = sys.stdin.readline()
marker = 0
for start, g in group(size, spec):
    if len(set(g)) == size:
        marker = start + size
        break

print(marker)