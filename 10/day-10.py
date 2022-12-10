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

chars = []
for i, s in signals_with_idx[1:]:
    pos = i - 1
    pos %= 40
    if s - 1 <= pos <= s + 1:
        chars.append('#')
    else:
        chars.append('.')

for i in range(0, len(chars), 40):
    print(''.join(chars[i:i+40]))
