import sys
import operator

operators = {
    '+': operator.__add__,
    '-': operator.__sub__,
    '*': operator.__mul__,
    '/': operator.__ifloordiv__,
    '=': operator.eq
}

monkeys = {}
to_check = int(sys.argv[1])
print(to_check)

for line in sys.stdin:
    parts = line.split()
    name = parts[0].rstrip(':')

    if len(parts) > 2:
        a, opkey, b = parts[1:]
        if name == 'root':
            opkey = '='

        op = operators[opkey]
        monkeys[name] = lambda a=a, op=op, b=b: op(monkeys[a](), monkeys[b]())

    else:
        val = int(parts[1])

        if name == 'humn':
            val = to_check
            
        monkeys[name] = lambda val=val: val

print(monkeys['root']())