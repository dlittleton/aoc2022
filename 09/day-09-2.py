import sys

def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

def move_tail(h, t):
    tx, ty = t
    diff_x = h[0] - tx
    diff_y = h[1] - ty
    
    if abs(diff_x) > 1:
        tx += sign(diff_x)
        if (diff_y != 0):
            ty += sign(diff_y)
    elif abs(diff_y) > 1:
        ty += sign(diff_y)
        if (diff_x != 0):
            tx += sign(diff_x)

    return (tx, ty)


knots = [(0, 0)] * 10
print(knots)
visited = set()

for l in map(str.rstrip, sys.stdin):
    dir, n = l.split(' ')

    for i in range(int(n)):
        head = knots[0]
        if dir == 'R':
            head = (head[0], head[1] + 1)
        elif dir == 'U':
            head = (head[0] - 1, head[1])
        elif dir == 'L':
            head = (head[0], head[1] - 1)
        elif dir == 'D':
            head = (head[0] + 1, head[-1])

        knots[0] = head
        for k in range(1, len(knots)):
            knots[k] = move_tail(knots[k - 1], knots[k])
        
        visited.add(knots[-1])

print(len(visited))