import sys

current = 1
signals = [0]

for line in map(str.rstrip, sys.stdin):
    cmd, *args = line.split(' ')
    if cmd == 'noop':
        signals.append(current)
    elif cmd == 'addx':
        signals.append(current)
        signals.append(current)
        current += int(args[0])
    
signals_with_idx = [(i, s) for i, s in enumerate(signals)]

total = 0
for i in range(20, len(signals_with_idx), 40):
    idx, sig = signals_with_idx[i]
    total += idx * sig

print(total)