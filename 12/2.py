import sys
import copy
import numpy as np
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def read_coords(s):
    s = s[1:-1]
    each = s.split(', ')
    x = int(each[0].split('=')[1])
    y = int(each[1].split('=')[1])
    z = int(each[2].split('=')[1])
    return [x,y,z]

def print_step(positions,velocities,step):
    max_len = 3
    print('After',step,'steps:')
    for i in range(len(positions)):
        x_pos = str(positions[i][0])
        y_pos = str(positions[i][1])
        z_pos = str(positions[i][2])
        x_vel = str(velocities[i][0])
        y_vel = str(velocities[i][1])
        z_vel = str(velocities[i][2])
        print('pos=<x='+' '*(max_len-len(x_pos))+x_pos+', y='+' '*(max_len-len(y_pos))+y_pos+', z='+' '*(max_len-len(z_pos))+z_pos+'>,',end=' ')
        print('vel=<x='+' '*(max_len-len(x_vel))+x_vel+', y='+' '*(max_len-len(y_vel))+y_vel+', z='+' '*(max_len-len(z_vel))+z_vel+'>')

    print()

def main(in_string):
    strings = in_string.strip().split('\n')

    positions = []
    velocities = []

    for s in strings:
        pos = read_coords(s)
        veloc = [0,0,0]
        positions.append(pos)
        velocities.append(veloc)

    snapshots = []
    diff_set = []
    start = []
    for i in range(len(positions)):
        snapshots.append([])
        snapshots[i].append((copy.deepcopy(positions[i]),copy.deepcopy(velocities[i])))
        start.append((copy.deepcopy(positions[i]),copy.deepcopy(velocities[i])))
        diff_set.append(set([]))



    time_step = 1
    found = False
    # previous diff_set
    prev = [None,None,None,None]
    # number of times we have seen the same previous diff set in a row
    prev_count = 0

    x_loop_pos = None
    y_loop_pos = None
    z_loop_pos = None

    x_loop_vel = None
    y_loop_vel = None
    z_loop_vel = None

    while True:
        # update velocities
        for idx, pos in enumerate(positions):
            for idy in range(idx,len(positions)):
                if not idx == idy:
                    other_pos = positions[idy]
                    # update x velocity
                    if other_pos[0] > pos[0]:
                        velocities[idx][0] += 1
                        velocities[idy][0] -= 1
                    elif other_pos[0] < pos[0]:
                        velocities[idx][0] -= 1
                        velocities[idy][0] += 1
                    # update y velocity
                    if other_pos[1] > pos[1]:
                        velocities[idx][1] += 1
                        velocities[idy][1] -= 1
                    elif other_pos[1] < pos[1]:
                        velocities[idx][1] -= 1
                        velocities[idy][1] += 1
                    # update z velocity
                    if other_pos[2] > pos[2]:
                        velocities[idx][2] += 1
                        velocities[idy][2] -= 1
                    elif other_pos[2] < pos[2]:
                        velocities[idx][2] -= 1
                        velocities[idy][2] += 1
        # update positions
        matchx = True
        matchy = True
        matchz = True
        matchxv = True
        matchyv = True
        matchzv = True
        for i in range(len(positions)):
            positions[i][0] += velocities[i][0]
            positions[i][1] += velocities[i][1]
            positions[i][2] += velocities[i][2]
            '''
            if not velocities[i] == start[i][1]:
                match = False
            '''
            if x_loop_pos == None:
                if not positions[i][0] == start[i][0][0]:
                    matchx = False
            if y_loop_pos == None:
                if not positions[i][1] == start[i][0][1]:
                    matchy = False
            if z_loop_pos == None:
                if not positions[i][2] == start[i][0][2]:
                    matchz = False
            if x_loop_vel == None:
                if not velocities[i][0] == start[i][1][0]:
                    matchxv = False
            if y_loop_vel == None:
                if not velocities[i][1] == start[i][1][1]:
                    matchyv = False
            if z_loop_vel == None:
                if not velocities[i][2] == start[i][1][2]:
                    matchzv = False
            '''
            snap_vel = [vel for (pos,vel) in snapshots[i]]
            if velocities[i] in snap_vel:
                prev_found_indexes = [ix for ix,val in enumerate(snap_vel) if val == velocities[i]]
                diffs = [time_step-prev for prev in prev_found_indexes]
                if len(diff_set[i]) == 0:
                    diff_set[i] = set(diffs)
                else:
                    diff_set[i] = diff_set[i] & set(diffs)


            snapshots[i].append((positions[i][:],velocities[i][:]))
            '''
        if x_loop_pos == None:
            if matchx == True and sum([0 if vel[0] == 0 else 1 for vel in velocities]) == 0:
                print('matched x timestep',time_step)
                x_loop_pos = time_step
        if y_loop_pos == None:
            if matchy == True and sum([0 if vel[1] == 0 else 1 for vel in velocities]) == 0:
                print('matched y timestep',time_step)
                y_loop_pos = time_step
        if z_loop_pos == None:
            if matchz == True and sum([0 if vel[2] == 0 else 1 for vel in velocities]) == 0:
                print('matched z timestep',time_step)
                z_loop_pos = time_step

        if x_loop_vel == None:
            if matchxv == True:
                print('matched vel x timestep',time_step)
                x_loop_vel = time_step
        if y_loop_vel == None:
            if matchyv == True:
                print('matched vel y timestep',time_step)
                y_loop_vel = time_step
        if z_loop_vel == None:
            if matchzv == True:
                print('matched vel z timestep',time_step)
                z_loop_vel = time_step

        if not x_loop_pos == None and not y_loop_pos == None and not z_loop_pos == None and not x_loop_vel == None and not y_loop_vel == None and not z_loop_vel == None:
            break

        time_step += 1

    lcm_pos = np.lcm.reduce([x_loop_pos,y_loop_pos,z_loop_pos,x_loop_vel,y_loop_vel,z_loop_vel])
    print(lcm_pos)

    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
