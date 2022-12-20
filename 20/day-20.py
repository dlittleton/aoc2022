import sys

class Wrap:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

original = [Wrap(int(l.rstrip())) for l in sys.stdin]
working = original[:]

zero = next(filter(lambda x: x.value == 0, original))

def cycle_idx(start, shift):
    return (start + shift) % len(working)

for o in original:
    position = working.index(o)

    del working[position]

    new_position = cycle_idx(position, o.value)
    working.insert(new_position, o)

zpos = working.index(zero)

a = working[cycle_idx(zpos, 1000)]
b = working[cycle_idx(zpos, 2000)]
c = working[cycle_idx(zpos, 3000)]

print(a, b, c)
print(a.value + b.value + c.value)

    