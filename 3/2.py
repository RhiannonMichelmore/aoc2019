import sys
sys.path.insert(1,'/home/rhiba/aoc2019/utils')

def main(in_string):
    wires = in_string.split('\n')
    wire_instrs = [path.split(',') for path in wires]

    # wire_coords[wire_num] = [coord list]
    # up = +y
    # down = -y
    # right = +x
    # left = -x
    wire_coords = []
    for i,path in enumerate(wire_instrs):
        wire_coords.append([(0,0)])
        for instr in path:
            direction = instr[0]
            amount = int(instr[1:])
            for j in range(1,amount+1):
                prev_coord = wire_coords[i][-1]
                if direction == 'U':
                    new_coord = (prev_coord[0],prev_coord[1] + 1)
                elif direction == 'R':
                    new_coord = (prev_coord[0] + 1, prev_coord[1])
                elif direction == 'D':
                    new_coord = (prev_coord[0],prev_coord[1] - 1)
                elif direction == 'L':
                    new_coord = (prev_coord[0] - 1, prev_coord[1])
                else:
                    print('uh oh')
                wire_coords[i].append(new_coord)

    # now check coord lists for duplicates
    res = list(set(wire_coords[0]) & set(wire_coords[1]))

    # now get min number of steps
    curr_min = None
    for (x,y) in res:
        if not (x==0 and y==0):
            steps_w1 = wire_coords[0].index((x,y))
            steps_w2 = wire_coords[1].index((x,y))
            steps = steps_w1 + steps_w2
            if curr_min == None:
                curr_min = steps
            elif steps < curr_min:
                curr_min = steps

    print(curr_min)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
