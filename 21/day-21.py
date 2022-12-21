import sys
import operator

operators = {
    '+': operator.__add__,
    '-': operator.__sub__,
    '*': operator.__mul__,
    '/': operator.__ifloordiv__,
}

monkeys = {}

for line in sys.stdin:
    parts = line.split()
    name = parts[0].rstrip(':')

    if len(parts) > 2:
        a, opkey, b = parts[1:]
        op = operators[opkey]
        monkeys[name] = lambda a=a, op=op, b=b: op(monkeys[a](), monkeys[b]())

    else:
        val = int(parts[1])
        monkeys[name] = lambda val=val: val

print(monkeys['root']())