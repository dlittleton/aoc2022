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
    pruned = dict(dup=0, max_production=0, projected_better=0)
    
    best_for_time = {}
    for i in range(turns):
        best_for_time[i] = (0,0,0,0)

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

        # Depth reached
        if t >= turns:
            if ag > geodes:
                geodes = ag
            continue

        # Increment for children nodes
        no = ao + bo
        nc = ac + bc
        nob = aob + bob
        ng = ag + bg
        nt = t + 1
        rt = turns - t

        # Prune node if the best state seen at this time has a better projected value than the current node
        zo, zc, zob, zg = best_for_time[t]
        po = ao + (bo * rt)
        pc = ac + (bc * rt)
        pob = aob + (bob * rt)
        pg = ag + (bg * rt)
        if zo > po and zc > pc and zob > pob and zg > pg:
            pruned['projected_better'] += 1
            continue
        elif pg > zg:
            best_for_time[t] = (po, pc, pob, pg)

        # Do nothing this turn
        heads.append((no, nc, nob, ng, bo, bc, bob, bg, nt))

        # Produce Ore Robot
        ore_available = ao + (bo *rt)
        ore_use = max_ore * rt
        if ore_available < ore_use:
            if ao >= ore_ore:
                heads.append((no - ore_ore, nc, nob, ng, bo + 1, bc, bob, bg, nt))
        else:
            pruned['max_production'] += 1

        # Produce Clay Robot
        clay_available = ac + (bc *rt)
        clay_use = obs_clay * rt
        if clay_available < clay_use:
            if ao >= clay_ore:
                heads.append((no - clay_ore, nc, nob, ng, bo, bc + 1, bob, bg, nt))
        else:
            pruned['max_production'] += 1

        # Produce Obsidian Robot
        obs_available = aob + (bob * rt)
        obs_use = geode_obs * rt
        if obs_available < obs_use:
            if bob < geode_obs and ao >= obs_ore and ac >= obs_clay:
                heads.append((no - obs_ore, nc - obs_clay, nob, ng, bo, bc, bob + 1, bg, nt))
        else:
            pruned['max_production'] += 1

        # Produce Geode Robot
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

