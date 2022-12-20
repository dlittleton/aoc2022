import re
import sys

import cProfile

numbers_re = re.compile(r'(\d+)')

def simulate(turns, idx, ore_ore, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs):
    ''' State is:
    
    Available Ore
              Clay
              Obsidian
              Geodes
    Producing Ore
              Clay
              Obsidian
              Geodes
    Depth
    '''
    seen = set()
    geodes = 0
    pruned = dict(dup=0, max_production=0)

    # Maximum ore used for a robot
    max_ore = max(ore_ore, clay_ore, obs_ore, geode_ore)
    
    heads = [(0,0,0,0,1,0,0,0,0)]
    while heads:
        state = heads.pop()
        
        # Prune already visited states
        if state in seen:
            pruned['dup'] += 1
            continue
        else:
            seen.add(state)
        
        ao, ac, aob, ag, bo, bc, bob, bg, t = state
        
        # Increment for children nodes
        no = ao + bo
        nc = ac + bc
        nob = aob + bob
        ng = ag + bg
        nt = t + 1
        rt = turns - t

        # Depth reached
        if t >= turns:
            if ag > geodes:
                geodes = ag
            continue

        heads.append((no, nc, nob, ng, bo, bc, bob, bg, nt))

        if ao >= ore_ore:
            max_use = max_ore * rt
            avail = ao + (bo * rt)
            if avail < max_use:
                heads.append((no - ore_ore, nc, nob, ng, bo + 1, bc, bob, bg, nt))
            else:
                pruned['max_production'] += 1

        if ao >= clay_ore:
            max_use = obs_clay* rt
            avail = ac + (bc * rt)
            if avail < max_use:
                heads.append((no - clay_ore, nc, nob, ng, bo, bc + 1, bob, bg, nt))
            else:
                pruned['max_production'] += 1

        if bob < geode_obs and ao >= obs_ore and ac >= obs_clay:
            max_use = geode_obs * rt
            avail = aob + (bob * rt)
            if avail < max_use:
                heads.append((no - obs_ore, nc - obs_clay, nob, ng, bo, bc, bob + 1, bg, nt))
            else:
                pruned['max_production'] += 1

        if ao >= geode_ore and aob >= geode_obs:
            heads.append((no - geode_ore, nc, nob - geode_obs, ng, bo, bc, bob, bg + 1, nt))

    print('Visited {0}'.format(len(seen)))
    print('Pruned {0}'.format(pruned))
    return geodes


def do_work():
    for line in map(str.rstrip, sys.stdin):
        result = simulate(24, *map(int, numbers_re.findall(line)))
        
        print(result)
        sys.stdout.flush()


cProfile.run('do_work()')

