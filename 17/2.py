import sys
import itertools
sys.path.insert(1,'/home/rhiba/aoc2019/utils')
import intcode
import copy

def occurances(whole_seq, seq):
	count = 0
	start = 0
	while True:
		if start + len(seq) > len(whole_seq):
			return count
		if whole_seq[start:start+len(seq)] == seq:
			count += 1
		start += 1

def pretty_print(grid):
    for row in grid:
        for item in row:
            print(item,end='')
        print()
    print()

def robot_char(rface):
    if rface == 'N':
        return '^'
    elif rface == 'E':
        return '>'
    elif rface == 'S':
        return 'v'
    else:
        return '<'

def get_dir(grid,rloc,rface):
    x = rloc[0]
    y = rloc[1]
    found = False
    if x-1 >= 0:
        if grid[y][x-1] == '#':
            card = 'W'
            found = True
    if x+1 < len(grid[0]):
        if grid[y][x+1] == '#':
            card = 'E'
            found = True
    if y-1 >= 0:
        if grid[y-1][x] == '#':
            card = 'N'
            found = True
    if y+1 < len(grid):
        if grid[y+1][x] == '#':
            card = 'S'
            found = True

    if found == False:
        return -1,-1

    if card == 'N':
        if rface == 'E':
            direc = 'L'
        elif rface == 'W':
            direc = 'R'
    elif card == 'E':
        if rface == 'N':
            direc = 'R'
        elif rface == 'S':
            direc = 'L'
    elif card == 'S':
        if rface == 'E':
            direc = 'R'
        elif rface == 'W':
            direc = 'L'
    elif card == 'W':
        if rface == 'S':
            direc = 'R'
        elif rface == 'N':
            direc = 'L'

    return card, direc


def main(in_string):
    ops = list(map(int,in_string.split(',')))
    orig_ops = copy.deepcopy(ops)
    position = 0
    relbase = 0
    inputs = []
    outputs = []
    while position >= 0:
        position, relbase = intcode.operate(position, relbase, ops, inputs, outputs)

    grid = []
    current_line = []
    rloc = None
    rface = None
    for output in outputs:
        if output == 10:
            if len(current_line) > 0:
                grid.append(current_line)
            current_line = []
        else:
            o = str(chr(output))
            if o == '<':
                rloc = (len(current_line),len(grid))
                rface = 'W'
            elif o == '^':
                rloc = (len(current_line),len(grid))
                rface = 'N'
            elif o == '>':
                rloc = (len(current_line),len(grid))
                rface = 'E'
            elif o == 'v':
                rloc = (len(current_line),len(grid))
                rface = 'S'
            current_line.append(o)

    intersections = []
    for y,row in enumerate(grid):
        for x,item in enumerate(row):
            if item == '#':
                inter = True
                if x - 1 >= 0:
                    if not grid[y][x-1] == '#':
                        inter = False
                else:
                    inter = False
                if x + 1 < len(row):
                    if not grid[y][x+1] == '#':
                        inter = False
                else:
                    inter = False
                if y - 1 >= 0:
                    if not grid[y-1][x] == '#':
                        inter = False
                else:
                    inter = False
                if y + 1 < len(grid):
                    if not grid[y+1][x] == '#':
                        inter = False
                else:
                    inter = False

                if inter == True:
                    intersections.append((x,y))

    #pretty_print(grid)
    orig_grid = copy.deepcopy(grid)

    # figure out what direction to turn and how far to go
    dir_list = []
    while True:
        cardinal, relative = get_dir(grid,rloc,rface) 
        if cardinal == -1:
            break
        steps = 0
        while True:
            x = rloc[0]
            y = rloc[1]
            if cardinal == 'N':
                if y-1 >= 0:
                    if grid[y-1][x] == '#':
                        if not (x,y) in intersections:
                            grid[y][x] = 'O'
                        rloc = (x,y-1)
                    else:
                        grid[y][x] = robot_char(cardinal)
                        rface = cardinal
                        rloc = (x,y)
                        break
                else:
                    grid[y][x] = robot_char(cardinal)
                    rface = cardinal
                    rloc = (x,y)
                    break
            elif cardinal == 'S':
                if y+1 < len(grid):
                    if grid[y+1][x] == '#':
                        if not (x,y) in intersections:
                            grid[y][x] = 'O'
                        rloc = (x,y+1)
                    else:
                        grid[y][x] = robot_char(cardinal)
                        rface = cardinal
                        rloc = (x,y)
                        break
                else:
                    grid[y][x] = robot_char(cardinal)
                    rface = cardinal
                    rloc = (x,y)
                    break
            elif cardinal == 'W':
                if x-1 >= 0:
                    if grid[y][x-1] == '#':
                        if not (x,y) in intersections:
                            grid[y][x] = 'O'
                        rloc = (x-1,y)
                    else:
                        grid[y][x] = robot_char(cardinal)
                        rface = cardinal
                        rloc = (x,y)
                        break
                else:
                    grid[y][x] = robot_char(cardinal)
                    rface = cardinal
                    rloc = (x,y)
                    break
            elif cardinal == 'E':
                if x+1 < len(grid[0]):
                    if grid[y][x+1] == '#':
                        if not (x,y) in intersections:
                            grid[y][x] = 'O'
                        rloc = (x+1,y)
                    else:
                        grid[y][x] = robot_char(cardinal)
                        rface = cardinal
                        rloc = (x,y)
                        break
                else:
                    grid[y][x] = robot_char(cardinal)
                    rface = cardinal
                    rloc = (x,y)
                    break
            steps += 1
        instruction = (relative,steps)
        dir_list.append(instruction)
    #pretty_print(grid)

    print(dir_list)
    repeat_seqs = []
    seen_subs = []
    for i in range(len(dir_list)):
        for l in range(1,len(dir_list)-i):
            sub = dir_list[i:i+l]
            if not sub in seen_subs:
                occ = occurances(dir_list,sub)
                repeat_seqs.append((occ,sub))	
                seen_subs.append(sub)
                    
    fixed_cost = 4
    max_cost = 20

    consider = []
    for r in repeat_seqs:
        if r[0] >= 2:
            if len(r[1])*fixed_cost <= max_cost:
                consider.append(r[1])

    # get every possible set of 3 in the consider set
    combs = list(itertools.combinations(consider,3))
    abc = None
    for c in combs:
        # see if we can "cover" the dir_list with these three direction sets
        found = False
        idx = 0
        order = []
        while True:
            if idx >= len(dir_list):
                # found match
                found = True
                abc = c
                break
            if idx+len(c[0]) <= len(dir_list) and dir_list[idx:idx+len(c[0])] == c[0]:
                idx = idx+len(c[0])
                order.append('A')
            elif idx+len(c[1]) <= len(dir_list) and dir_list[idx:idx+len(c[1])] == c[1]:
                idx = idx+len(c[1])
                order.append('B')
            elif idx+len(c[2]) <= len(dir_list) and dir_list[idx:idx+len(c[2])] == c[2]:
                idx = idx+len(c[2])
                order.append('C')
            else:
                break

        if found == True:
            break

    print('Command A:',abc[0])
    print('Command B:',abc[1])
    print('Command C:',abc[2])
    print('Main sequence:',order)

    main_sequence = []
    for i,letter in enumerate(order):
        main_sequence.append(ord(letter))
        if i == len(order)-1:
            main_sequence.append(10)
        else:
            main_sequence.append(ord(','))

    print(main_sequence)

    commandA = []
    for i,pair in enumerate(abc[0]):
        commandA.append(ord(pair[0]))
        commandA.append(ord(','))
        string_num = str(pair[1])
        for char in string_num:
            commandA.append(ord(char))
        if i == len(abc[0])-1:
            commandA.append(10)
        else:
            commandA.append(ord(','))

    print(commandA)
    print(len(commandA))
    commandB = []
    for i,pair in enumerate(abc[1]):
        commandB.append(ord(pair[0]))
        commandB.append(ord(','))
        string_num = str(pair[1])
        for char in string_num:
            commandB.append(ord(char))
        if i == len(abc[1])-1:
            commandB.append(10)
        else:
            commandB.append(ord(','))

    print(commandB)
    print(len(commandB))
    commandC = []
    for i,pair in enumerate(abc[2]):
        commandC.append(ord(pair[0]))
        commandC.append(ord(','))
        string_num = str(pair[1])
        for char in string_num:
            commandC.append(ord(char))
        if i == len(abc[2])-1:
            commandC.append(10)
        else:
            commandC.append(ord(','))

    print(commandC)
    print(len(commandC))
    inputs = main_sequence + commandA + commandB + commandC + [ord('n'),10]

    ops = copy.deepcopy(orig_ops)
    ops[0] = 2
    position = 0
    relbase = 0
    outputs = []
    while position >= 0:
        position, relbase = intcode.operate(position, relbase, ops, inputs, outputs)

    print(outputs)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No input found.')
    else:
        with open(sys.argv[1],'r') as f:
            in_string = f.read().strip()
            main(in_string)
