import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def read_coords(s):
    s = s[1:-1]
    each = s.split(', ')
    x = int(each[0].split('=')[1])
    y = int(each[1].split('=')[1])
    z = int(each[2].split('=')[1])
    return [x,y,z]

def main(in_string):
    strings = in_string.strip().split('\n')

    positions = []
    velocities = []

    for s in strings:
        pos = read_coords(s)
        veloc = [0,0,0]
        positions.append(pos)
        velocities.append(veloc)

    max_len = 3
    print('After 0 steps:')
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
    
    time_steps = 1000
    for t in range(1,time_steps+1):
        # update velocities
        for idx, pos in enumerate(positions):
            for idy, other_pos in enumerate(positions):
                if not idx == idy:
                    # ONLY UPDATE MOON || idx || HERE, otherwise double updates will happen
                    # update x velocity
                    if other_pos[0] > pos[0]:
                        velocities[idx][0] += 1
                    elif other_pos[0] < pos[0]:
                        velocities[idx][0] -= 1
                    # update y velocity
                    if other_pos[1] > pos[1]:
                        velocities[idx][1] += 1
                    elif other_pos[1] < pos[1]:
                        velocities[idx][1] -= 1
                    # update z velocity
                    if other_pos[2] > pos[2]:
                        velocities[idx][2] += 1
                    elif other_pos[2] < pos[2]:
                        velocities[idx][2] -= 1
        # update positions
        for i in range(len(positions)):
            positions[i][0] += velocities[i][0]
            positions[i][1] += velocities[i][1]
            positions[i][2] += velocities[i][2]

        print('After',t,'steps:')
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

    potentials = []
    kinetics = []
    for i in range(len(positions)):
        pot = abs(positions[i][0])+abs(positions[i][1])+abs(positions[i][2])
        kin = abs(velocities[i][0])+abs(velocities[i][1])+abs(velocities[i][2])
        potentials.append(pot)
        kinetics.append(kin)

    sum_tot = sum([x*y for (x,y) in zip(potentials,kinetics)])
    print('Sum of total:',sum_tot)




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
