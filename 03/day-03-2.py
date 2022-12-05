import sys

def get_priority(x):
    if 'a' <= x <= 'z':
        return (ord(x) - ord('a')) + 1
    else:
        return (ord(x) - ord('A')) + 27

rucksacks = [set(line) for line in map(str.rstrip, sys.stdin)]

total = 0
while rucksacks:
    a = rucksacks.pop()
    b = rucksacks.pop()
    c = rucksacks.pop()
    common = (a & b & c).pop()
    total += get_priority(common)

print(total)
