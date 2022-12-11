import sys

def parse_position(l):
    _, pos = l.split(' ')
    pos = pos.rstrip(':')
    return int(pos)

def parse_items(l):
    _, items = l.split(':')
    return [int(i) for i in items.split(',')]

def parse_operation(l):
    _, op = l.split('=')
    return lambda old: eval(op)

def parse_last_int(l):
    tokens = l.split(' ')
    return int(tokens[-1])

class Monkey:
    def __init__(self, spec):
        self.pos = parse_position(spec[0])
        self.items = parse_items(spec[1])
        self.op = parse_operation(spec[2])
        self.test = parse_last_int(spec[3])
        self.on_true = parse_last_int(spec[4])
        self.on_false = parse_last_int(spec[5])
        self.inspected = 0

    def toss_items(self):
        copy = self.items
        self.items = []

        for item in copy:
            self.inspected += 1
            inspected = self.op(item)
            relieved = inspected // 3
            target = self.on_true if relieved % self.test == 0 else self.on_false

            yield(target, relieved)


lines = [l.rstrip() for l in sys.stdin]
monkeys = [Monkey(lines[i:i+6]) for i in range(0, len(lines), 7)]

rounds = 20
for i in range(rounds):
    for m in monkeys:
        for pos, value in m.toss_items():
            monkeys[pos].items.append(value)

top = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
print(top[0].inspected * top[1].inspected)