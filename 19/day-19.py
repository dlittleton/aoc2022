import operator
import re
import sys

from collections import namedtuple, deque

numbers_re = re.compile(r'(\d+)')

class Resources(namedtuple('Resources', ['ore', 'clay', 'obsidian', 'geode'])):
    
    def __add__(self, other):
        return Resources(*self.apply(operator.add, other))

    def __sub__(self, other):
        return Resources(*self.apply(operator.sub, other))

    def __gt__(self, other):
        return all(self.apply(operator.gt, other))

    def __ge__(self, other):
        return all(self.apply(operator.ge, other))

    def apply(self, op, other, ):
        return (op(a, b) for a, b in zip(self, other))

class Factory:

    def __init__(self, blueprint, ore, clay, obsidian, geode):
        self.blueprint = blueprint
        
        self.costs = [ore, clay, obsidian, geode]
        self.production = [Resources(1,0,0,0), Resources(0,1,0,0), Resources(0,0,1,0), Resources(0,0,0,1)]

        self.max_ore = max(r.ore for r in self.costs)
        self.max_clay = max(r.clay for r in self.costs)
        self.max_obsidian = max(r.obsidian for r in self.costs)

    def simulate(self, turns):
        available = Resources(0, 0, 0, 0)
        bots = Resources(1, 0, 0, 0)

        seen = set()
        geodes = 0
        pruned = 0

        best = {}
        for i in range(turns):
            best[i] = (Resources(0,0,0,0), Resources(0,0,0,0))

        heads = [(available, bots, 0)]
        while heads:
            state = heads.pop()
            if state in seen:
                pruned += 1
                continue
            else:
                seen.add(state)

            cur_available, cur_bots, cur_time = state

            # Check for depth
            if cur_time >= turns:
                geodes = max(geodes, cur_available.geode)
                continue

            best_available, best_bots = best[cur_time]
            if best_available >= cur_available and best_bots >= cur_bots:
                continue
            elif cur_available >= best_available and cur_bots >= best_bots:
                best[cur_time] = (cur_available, cur_bots)

            # Produce ore
            next_available = cur_available + cur_bots

            if cur_bots.ore < self.max_ore and cur_available >= self.costs[0]:
                heads.append((next_available - self.costs[0], cur_bots + self.production[0], cur_time + 1))

            if cur_bots.clay < self.max_clay and cur_available >= self.costs[1]:
                heads.append((next_available - self.costs[1], cur_bots + self.production[1], cur_time + 1))

            if cur_bots.obsidian < self.max_obsidian and cur_available >= self.costs[2]:
                heads.append((next_available - self.costs[2], cur_bots + self.production[2], cur_time + 1))

            if cur_available >= self.costs[3]:
                heads.append((next_available - self.costs[3], cur_bots + self.production[3], cur_time + 1))

            # Skip making bots
            heads.append((next_available, cur_bots, cur_time + 1))

        print('Visited {0}, Pruned {1}'.format(len(seen), pruned))
        return geodes



for line in map(str.rstrip, sys.stdin):
    idx, ore_ore, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs = map(int, numbers_re.findall(line))
    ore = Resources(ore_ore, 0, 0, 0)
    clay = Resources(clay_ore, 0, 0, 0)
    obsidian = Resources(obs_ore, obs_clay, 0, 0)
    geode = Resources(geode_ore, 0, geode_obs, 0)

    factory = Factory(idx, ore, clay, obsidian, geode)
    test = factory.simulate(24)
    print(test)
    sys.stdout.flush()

