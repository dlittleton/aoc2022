import sys
import operator

operators = {
    '+': operator.__add__,
    '-': operator.__sub__,
    '*': operator.__mul__,
    '/': operator.__ifloordiv__,
}

inverse = {
    '+': '-',
    '-': '+',
    '*': '/',
    '/': '*'
}

monkeys = {}
for line in sys.stdin:
    name, *rem = line.split()
    name = name.rstrip(':')

    monkeys[name] = int(rem[0]) if len(rem) == 1 else rem

# Replace root equation
a, _, b = monkeys['root']
monkeys['root'] = [a, '=', b]

# Replace humn value
monkeys['humn'] = 'x'

def simplify(key):
    expr = monkeys[key]
    if type(expr) != list:
        return expr

    a, op, b = expr
    first = simplify(a)
    second = simplify(b)

    if type(first) == int and type(second) == int:
        return operators[op](first, second)

    
    return (op, first, second)


op, a, b = simplify('root')

def sort_terms(a, b):
    return (a, b) if type(a) == int else (b, a)
target, expr = sort_terms(a, b)

def evaluate(target, expr):
    opkey, a, b = expr
    inv = inverse[opkey]

    # Division and subtraction are not commutative
    if opkey in ['-', '/'] and type(b) == tuple:
        new_expr = (inv, target, b)
        new_target = a
        print('Replacing target with ', new_target)
        return evaluate(new_target, new_expr)

    term, rest = sort_terms(a, b)
    op = operators[inv]

    target = op(target, term)

    return evaluate(target, rest) if type(rest) == tuple else target

result = evaluate(target, expr)
print(result)
    



