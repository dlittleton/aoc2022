import re
import sys

import cProfile

from math import ceil

numbers_re = re.compile(r'(\d+)')

def describe_path(path):
    prev = path[0]
    for p in path[1:]:
        ao, ac, aob, ag, bo, bc, bob, bg, t = prev
        for i in range(t, p[-1]):
            ao += bo
            ac += bc
            aob += bob
            ag += bg
            print('== Minute {0} =='.format(i))
            print('collect {0} ore; now have {1} ore'.format(bo, ao))
            print('collect {0} clay; now have {1} clay'.format(bc, ac))
            print('collect {0} obsidian; now have {1} obsidian'.format(bob, aob))
            print('collect {0} geodes; now have {1} geodes'.format(bg, ag))

            print()
        print('########')
        prev = p


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
    geodes = 0
    best_path = []
    pruned = dict(dup=0, max_production=0)

    # Maximum ore used for a robot
    max_ore = max(ore_ore, clay_ore, obs_ore, geode_ore)
    
    heads = [(0,0,0,0,1,0,0,0,1,[])]
    while heads:
        state = heads.pop()
        
        ao, ac, aob, ag, bo, bc, bob, bg, t, path = state

        child_path = path[:]
        child_path.append((ao, ac, aob, ag, bo, bc, bob, bg, t))

        #if bo == 2 and t < first_ore:
        #    print('Produced ore bot at time: ', t)
        #    print('\tAvailable: ', ao, ac, aob, ag)
        #    print('\tBots: ', bo, bc, bob, bg)
        #    print('\tEnd: ', ao + bo, ac + bc, aob + bob, ag + bg)
        #    sys.exit()

        #if t <= 13 and bc == 4:
        #    print('Produced clay bot at time: ', t)
        #    print('\tAvailable: ', ao, ac, aob, ag)
        #    print('\tBots: ', bo, bc, bob, bg)
        #    print('\tEnd: ', ao + bo, ac + bc, aob + bob, ag + bg)
        #    sys.exit()

        #if t <= 12 and bob == 1:
        #    print('Produced obs bot at time: ', t)
        #    print('\tAvailable: ', ao, ac, aob, ag)
        #    print('\tBots: ', bo, bc, bob, bg)
        #    print('\tEnd: ', ao + bo, ac + bc, aob + bob, ag + bg)
        #    sys.exit()

        #if t <= 19 and bg == 1:
        #    first_geode = t
        #    print('Produced geode bot at time: ', t)
        #    print('\tAvailable: ', ao, ac, aob, ag)
        #    print('\tBots: ', bo, bc, bob, bg)
        #    print('\tEnd: ', ao + bo, ac + bc, aob + bob, ag + bg)
        #    sys.exit()

        # Depth reached
        if t >= turns:
            if t > turns:
                raise RuntimeError('Broken!')
            if ag + bg > geodes:
                geodes = ag + bg
                best_path = child_path
            continue

        # Increment for children nodes
        rt = turns - t
        added = 0

        # Produce Ore Robot
        ore_available = ao + (bo *rt)
        ore_use = max_ore * rt
        if ore_available < ore_use:
            temp = turns
            for i in range(0, turns):
                if ao + (i * bo) >= ore_ore:
                    temp = i
                    break

            next_ore = temp + 1
            
            if next_ore <= rt:
                added += 1
                no = ao + (bo * next_ore)
                nc = ac + (bc * next_ore)
                nob = aob + (bob * next_ore)
                ng = ag + (bg * next_ore)
                heads.append((no - ore_ore, nc, nob, ng, bo + 1, bc, bob, bg, t + next_ore, child_path))
        else:
            pruned['max_production'] += 1

        # Produce Clay Robot
        clay_available = ac + (bc *rt)
        clay_use = obs_clay * rt
        if clay_available < clay_use:
            temp = turns
            for i in range(0, turns):
                if ao + (i * bo) >= clay_ore:
                    temp = i
                    break

            next_clay = temp + 1
            
            if next_clay <= rt:
                added += 1
                no = ao + (bo * next_clay)
                nc = ac + (bc * next_clay)
                nob = aob + (bob * next_clay)
                ng = ag + (bg * next_clay)
                heads.append((no - clay_ore, nc, nob, ng, bo, bc + 1, bob, bg, t + next_clay, child_path))
        else:
            pruned['max_production'] += 1

        # Produce Obsidian Robot
        obs_available = aob + (bob * rt)
        obs_use = geode_obs * rt
        if obs_available < obs_use and bc > 0:
            temp = turns
            for i in range(0, turns):
                if ao + (i * bo) >= obs_ore and ac + (i * bc) >= obs_clay:
                    temp = i
                    break

            next_obs = temp + 1

            if next_obs <= rt:
                added += 1
                no = ao + (bo * next_obs)
                nc = ac + (bc * next_obs)
                nob = aob + (bob * next_obs)
                ng = ag + (bg * next_obs)

                heads.append((no - obs_ore, nc - obs_clay, nob, ng, bo, bc, bob + 1, bg, t + next_obs, child_path))
        else:
            pruned['max_production'] += 1

        # Produce Geode Robot
        if bob > 0:
            temp = turns
            for i in range(0, turns):
                if ao + (i * bo) >= geode_ore and aob + (i * bob) >= geode_obs:
                    temp = i
                    break

            next_geode = temp + 1

            if next_geode <= rt:
                added += 1
                no = ao + (bo * next_geode)
                nc = ac + (bc * next_geode)
                nob = aob + (bob * next_geode)
                ng = ag + (bg * next_geode)

                heads.append((no - geode_ore, nc, nob - geode_obs, ng, bo, bc, bob, bg + 1, t + next_geode, child_path))

        # Finish out the path if geodes are being produced.
        if added == 0 and bg > 0:
            heads.append((ao + bo, ac + bc, aob + bob, ag + bg, bo, bc, bob, bg, t+1, child_path))         

    #print('Visited {0}'.format(len(seen)))
    #print('Pruned {0}'.format(pruned))
    #describe_path(best_path)
    return geodes


def do_work():
    for line in map(str.rstrip, sys.stdin.readlines()[0:3]):
        result = simulate(32, *map(int, numbers_re.findall(line)))
        
        print(result)
        sys.stdout.flush()


cProfile.run('do_work()')

