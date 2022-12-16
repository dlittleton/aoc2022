import sys
import re

from collections import deque

valve_re = re.compile(r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)')
max_depth = 30

class Valve:

    def __init__(self, name, rate, links):
        self.name = name
        self.rate = rate
        self.links = links
        self._travel = {}

    def travel(self, target, depth = 0):
        if target not in self._travel:
            children = deque((1, l) for l in self.links)
            while children:
                depth, name = children.popleft()
                if name not in self._travel:
                    self._travel[name] = depth
                    v = valves[name]
                    for link in v.links:
                        children.append((depth + 1, link))

        return self._travel[target]

def score(open):
    total = 0
    for key in open:
        rate = valves[key].rate
        open_time = open[key]
        total += max(max_depth - open_time, 0) * rate
    return total


def search(position, open={}, time=0, best=0):
    valve = valves[position]
    targets = working_valves - open.keys()

    if not targets or time > max_depth:
        return max(best, score(open))

    for t in targets:
        travel_time = valve.travel(t)
        new_time = time + travel_time + 1 
        new_open = open.copy()
        new_open[t] = new_time
        best = search(t, new_open, new_time, best)

    return best


valves = {}
for line in sys.stdin:
    m = valve_re.match(line)
    name, rate, links = m.groups()
    v = Valve(name, int(rate), [l.strip() for l in links.split(',')])
    valves[v.name] = v
working_valves = set(v.name for v in valves.values() if v.rate != 0)

result = search('AA')
print(result)




