import sys

values = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2
}

total = 0
for line in map(str.rstrip, sys.stdin):
    for position, char in enumerate(reversed(line)):
        total += values[char] * 5 ** position

answer = ''

while total:
    temp = total % 5
    if temp in (0, 1, 2):
        answer += str(temp)
        total //= 5
    elif temp == 3:
        answer += '='
        total //= 5
        total += 1
    elif temp == 4:
        answer += '-'
        total //= 5
        total += 1

print(''.join(reversed(answer)))